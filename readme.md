## Microsoft Job Handover
#### Content：
based on the existing job scheduler scheduling algorithm, explore the use of ML algorithms to improve the scheduling efficiency of data jobs
* Select feature on basis of business logic
* Select indicators for job scheduling system
* Consider the priority order of different inputs, sort and label jobs reasonably
* Perform feature engineering after marking, use appropriate model training, and adjust hyperparameters
* For a new job, use the model to predict its priority and compare it with the current scheduling results of Ares Scheduler based on quota management to analyze its rationality. And based on the analysis, add and reduce the feature, adjust the weight of the feature.

#### Features
* **YieldScopePriority_X**
    Reflect the importance of the job, yield can only occur when priorityX is higher
* **YieldScopePriority_Y**
    Under the same level of Priority_X, Priority_y determines the priority
* **Job Token**
    The amount of memory the job needs to occupy
* **AU Quota**
    The memory size of the current AU to which the job belongs. It is believed that the smaller the job token and the larger the AU Quota, the higher the priority given to the job, because the addition of the job itself has a smaller capacity for the system
     (jobs with large tokens will not always be blocked, since the waiting time increases, the priority will continue to increase)
* **Can be yielded**
    whether job can be yielded
* **Can yield others**
    whether job can yield others
    job which has yield ability have flexibility therefore have higher priority
* **Queuing Time**
    The time that the job has been waiting in the queue. The longer the job in the queue, the higher the priority.
* **Estimated Time**
    The estimated finished time of the job, which was estimated from previous similai job, depends on name pattern. The smaller the estimated time during the marking process, the higher the priority will be given
* **isAUfully**
    Whether the AU to which the job belongs is currently fully loaded, if the AU to which the job belongs is already fully loaded, the priority of the job should be lowered
* **SLA**
    Whether the job belongs to SLA job
    If an SLA job, increase its priority. Missing SLA is not considered in the process of labeling

#### label data
1. first divides the data into five major priority group
2. Expand the data of each category to make the data continuous
3. Consider the criticality of multiple groups and make slight adjustments

#### Model selection
##### Random Forest
The amount of data used for training is 1000 rows, and there are only more than ten related features after feature engineering processing, some of the features are classification features, therefore it is easy to think of using tree-based models
The random forest model is selected, that is, the idea of bagging is used to ensemble multiple decision trees. When dealing with regression tasks, there is only one tree classification algorithm, that is, the minimum square error algorithm, and plus the depth of the tree as the penalty function.
For the selection of hyperparameters, only the number of estimator and the maximum number of features of bootstrap are selected and have a cross-validation. When N_ESTIMATOR is greater than 225, the output tends to be stable, and the maximum number of features is 0.75, which means that the model has the lowest error.


#### Related data preprocessing
`sparse data`
The amount of data for some features in the input is small, for example, jobs with priority_Y greater than 2 (excluding null) are sparse. Considering that it has little effect on priority, merge them into the class of priority_y=2
`one-hot Encoding`
Some features are not numerically continuous features. For example, priority_y can be 0, 1, 2, 10, or null.
Encoding them with hot unique codes can effectively avoid solving the numerical problem of 10 and null, and can increase the number of features
`log(1+x)`
Smoothing function

#### Effectiveness analysis
**indicators** 
* Whether there are important jobs that are put on hold when the VC is high in usage
* whether any jobs that are queuing when there are some idle tokens?
* Delay time of important jobs (when job priorityX = 0/1)
######  Compare the scheduling results of two different methods
The initial method is to take out a part of the job and let the model predict its priority and compare it with the scheduling results of Ares Scheduler based on Quota management.
Analyze different reasons and rationality
######  cosmos_mock
Only looking at the priority results cannot know the cluster usage and other characteristics. And the scheduling results of a specific round of Ares Scheduler cannot be found in the database.
Therefore, Based on the logic of Ares Scheduler, a mock system has been built, and the information of 2 days of jobs (about 13000 jobs) is extracted for scheduling, and the usage of the cluster and the delay time of jobs are observed.


#### file description

`./job_scheduler_model2`：Feature engineer and model training
`./mock_run`:mock_system
`./data/data_v3_2`:labelled data in last time

# Environment setup
* python 3.7+
* use `jupyter Notebook` to open `.ipynb` file
