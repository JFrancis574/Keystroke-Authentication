from keyboardTest import *


data = [
    [
        ['h', 0.7170403003692627, 0.80442214012146], ['i', 0.8220560550689697, 0.8794219493865967], ['m', 0.9934704303741455, 1.09175443649292]
    ], 
    [
        ['b', 1.7434194087982178, 1.8060758113861084], ['y', 1.9234187602996826, 2.025184154510498]], [['g', 2.174997329711914, 2.24741792678833], ['o', 2.256417751312256, 2.334017515182495], ['v', 2.469417095184326, 2.547417163848877], ['e', 2.5684170722961426, 2.63144588470459], ['r', 2.7295496463775635, 2.8174164295196533]
    ], 
    [

    ],
    [
        ['w', 3.1230156421661377, 3.186415195465088], ['a', 3.2671329975128174, 3.3934144973754883], ['r', 3.357409715652466, 3.471414804458618], ['m', 3.5524139404296875, 3.699413537979126]
    ], 
    [
        ['d', 3.8755481243133545, 3.960014820098877], ['r', 4.09241247177124, 4.193789720535278], ['a', 5.619501352310181, 5.7453765869140625], ['w', 5.685410737991333, 5.817407131195068]
    ], 
    [
        ['m', 6.233533620834351, 6.314800262451172], ['a', 6.315744161605835, 6.3934056758880615], ['k', 6.446620225906372, 6.535956859588623], ['r', 6.522068977355957, 6.624404430389404]
    ], 
    [
        ['p', 7.373340129852295, 7.433179616928101], ['l', 7.528995752334595, 7.625018835067749], ['a', 7.58940315246582, 7.7450034618377686]], [['e', 8.203522205352783, 8.290601968765259]
    ], 
    [
        ['o', 8.702242374420166, 8.765076875686646], ['r', 9.076568365097046, 9.157963037490845]
    ], 
    [
        ['f', 9.350338697433472, 9.430727005004883], ['r', 9.548396110534668, 9.629395961761475], ['i', 9.688666343688965, 9.75839877128601]
    ]
]

for i, j in enumerate(data):
    print(i, j)
    
KDSWordByWord(data, 4)