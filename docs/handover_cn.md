## 微软工作交接
#### 内容：
对现有的job scheduler的调度算法进行了解，探究使用ML 算法提升data job的调度效率
* 根据业务逻辑选择feature
* 选取job调度的指标
* 思考不同输入的优先顺序，合理对jobs进行排序，并进行标记
* 完成标记后进行特征工程，使用合适的模型训练，调整超参数
* 对于新的job，使用模型预测其优先级，并和当前基于quota management的Ares Scheduler的调度结果对比，分析其合理性。并基于分析，添加减少feature，调整feature的权值。

#### feature的选取
* YieldScopePriority_X
    体现job的重要程度，只有priorityX高时才能发生yield
* YieldScopePriority_Y
    在同一级Priority_X下，priority_y决定优先级
* Job Token
    job所需要占用的内存大小
* AU Quota
    job所属的当前AU的内存大小，这里认为，job token越小，AU Quota越大，赋予job的优先级就越高，因为job的加入本身对系统的容量较小
    （对于大token的job并不会一直发生阻塞，因为随着等待时间的增加，优先级也会不断地提升）
* Can be yielded
    job是否能被yield
* Can yield others
    job能否yield其它的job，体现job的灵活性，赋予更高的优先级
    数据中，大部分的job都是可以被yield的，因此这两个feature不会过多影响优先级
* Queuing Time
    job在队列中已等待的时间，在队列中等待越久的job，其优先级越高
* Estimated Time
    job预估的完成时间，标记的过程中认为预估的时间越小，赋予的优先级越高
* isAUfully
    job所属AU当前是否已经满载，如果job所属的AU已经发生了满载，job的优先级应当降低
* SLA
    job是否属于SLA job
    如果是SLA job则提升其优先级。在label的过程中不考虑miss SLA的情况

#### 模型的选择
##### 随机森林
训练用的数据量为1000行，相关特征经过特征工程处理后只有十余个，而且部分特征是分类特征，因为很容易想到使用树节点类的模型
最终选择随机森林模型，即用bagging的思想集成多棵决策树。在处理回归任务时只有一种树分类算法，即最小平方误差算法，加上树的深度作为惩罚函数
超参数的选择，这里仅对决策器的个数和bootstrap的最大特征数量进行选择，做交叉验证，N_ESTIMATOR大于225时，输出趋于稳定，最大特征数为0.75是，模型的误差最低。


#### 相关数据预处理
`稀疏数据`
输入中部分特征的数据量较小，如priority_Y大于2的job（不包括null）较为稀疏。考虑其对优先级影响不大，将它们并入到priority_y=2的类中
`one-hot Encoding`
部分特征并不是数值连续的特征，如priority_y可以取0，1，2，10，null。
对它们使用热独码进行编码，可有效避免解决对10和null的数值问题，并能提升特征数量
`log(1+x)`
平滑函数

#### 有效性分析
**指标** 
* 高使用率时是否有重要的job被搁置
* 有空闲token时是否有小的job被搁置
* 重要jobs（PriorityX=0/1）的延迟时间
######  对比两种不同方法的排序结果
最初的方法是取出一部分job让模型预测其优先级并和基于Quota management的Ares Scheduler调度结果进行对比
分析不同的原因和合理性
######  cosmos_mock
仅看排序结果无法看出集群的使用率等特征，且数据库中无法找到特定某一轮Ares Scheduler的调度结果
基于Ares Scheduler的逻辑仿写了一个cosmos,提取2天的jobs(13000+)的信息进行调度，观察集群的使用情况和jobs的延迟时间


#### 文件说明

`./job_scheduler_model2`：特征工程和调参的具体步骤
`./mock_run`:仿写的mock系统
`./data/data_v3_2`:最后一次标记的data
