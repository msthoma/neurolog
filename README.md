Forked from the [neurolog repository](https://bitbucket.org/tsamoura/neurolog/src/master/), based on the paper by Tsamoura & Michael (2020), [_Neural-Symbolic Integration: A Compositional Perspective_](https://arxiv.org/abs/2010.11926).

The original README follows.

# README #

Contains the source code to reproduce the CHESS-BSV, CHESS-ISK and CHESS-NGA scenarios.
The source code has been developed in an Ubuntu Linux machine using Eclipse IDE version 2018-12 (4.10.0) and PyDev (https://www.pydev.org/). 

### Prerequisites ###

* Python >= 3.6.
* PyTorch (https://pytorch.org/).
* PySDD (https://github.com/wannesm/PySDD).
* SICStus Prolog (4.5.1 and higher https://sicstus.sics.se/download4.html).

### Folder structure ###

* "master" is the top-level folder.
* "src" includes the source code and one folder per test scenario, e.g., one folder for the add2x2 scenario, one for apply2x2, etc. Each scenario folder includes scripts to generate data and to perform training and testing. 
* "engine" includes an implementation of the A-system.
* "proofs" includes cached proofs to run CHESS-BSV and generate training and testing data.
* "theories" includes the theories related to each scenario.  
* "data" includes training and testing data.
* "models" (produced during training). 
* "logs" (produced during training). 
* "results" (produced during testing).

### Cached proofs ###
* Each one of the files "proofs/safe.txt", "proofs/draw.txt" and "proofs/mate.txt" store all the proofs that describe the corresponding 
condition. Each row in each file is of the form: 
[cost(.),at(b(k),(X1,Y1)),at(w(P1),(X2,Y2)),at(w(P2),(X3,Y3))], where "b(k)" denotes the black king, w(Pi) denotes a white piece, e.g., 
"q" for queen, and (Xj,Yj) are the coordinates of the pieces in the board. For example, the proof "[cost(30),at(b(k),(1,1)),at(w(b),(1,2)),at(w(k),(3,1))]." from the file "proofs/safe.txt" states that 
the black king is safe if it is in position (1,1), the white bishop is in (1,2) and the white king is in (3,1).
* Notice: these proofs can be optionally used in the chess-BSV scenario, but are always used for generating training and testing data.

### Naming conventions ###
* We use ? to denote either of "BSV", "ISK", or "NGA". 
* We use X to denote the different runs of training.
* We use SICSTUS_BIN to denote the full path to the bin folder of SICStus Prolog.

### Configuration ###
* Create a folder named "outputs" inside SICSTUS_BIN.
* Copy the file "engine/abduction.pl" inside SICSTUS_BIN.
* Replace SICSTUS_BIN in the files under "theories" by the actual full path of the bin folder.
* Copy the files under "theories" inside SICSTUS_BIN.
* Set the variable sicstus\_bin in the file "src/params.pl" to the full path of the bin folder of SICStus Prolog.
* Choose the desired number of epochs and number of training data in "src/params.pl" or use the default ones. 
* Warning: the visualization files have been tested for the default training and testing parameters.

### How to create training and testing data ###
* The top-level folder "data" *already* contains training and testing data, so no need to do anything. However, a generator is also available under each scenario folder. 
* Warning: "src/chess/generate.py" consumes proofs from the top-level folder named "proofs", so do not modify this folder.

### Assumptions ###

* In the CHESS scenarios, we consider a 3x3 chess board, which has exactly three pieces each time one of which is the black king and the two others are white pieces. Furthermore, the black king should not threat the white king and vice versa. 

### How to train ###
* Run the "scenario_traing.py" in each scenario folder, e.g., "src/add2x2/scenario_train.py". 
* For the CHESS scenarios, execute the file "src/run/scenario_traing.py" after choosing the right scenario "BSV", "ISK", or "NGA".
* Training is done 5 times in total.

### Training without calling SICStus ###
* To provide an easy to run POC, we modified the "BSV" scenario to work without calling SICStus Prolog. This scenario works by reading the cached proofs inside the "proofs" folder. This scenario can be modified to run using SICStus Prolog by 
modifying the file "chess/abduction/chessBSV.py" so that 
the *abduce* method in lines 27--48 is commented out. 
* Warning: "abduction/chessBSV.py" consumes proofs from the top-level folder named "proofs", so do not modify this folder unless the file is modified to run using SICStus Prolog.
* All the other scenarios including chess-ISK and chess-NGA require calling SICStus Prolog.  

### Outputs of the training step ###
* The computed models inside the "models/?/X" directory, where X denotes the run.
* A "log.txt" file inside the "logs/?" directory. Each line in each file "log.txt" is of the form: iterations \t time-to-train-for-these-iterations. 

### How to test ###
* Execute the file "src/run/scenario_test.py" in each scenario folder, e.g., "src/add2x2/scenario_test.py".
* Warning: the file "src/run/scenario_test.py" reads the models produced during the training process.
 
### Outputs of the testing step ###
* The testing accuracy.
* In the chess scenarios, an "accuracy\_vs\_iter\_X.txt" file inside the "results/?" directory, where X denotes the run. Each line in each file "accuracy\_vs\_iter_X.txt" is of the form: iterations \t accuracy-for-these-iterations. 

### Visualising the results for the CHESS scenarios ###
* Execute the file "src/visualisation/accuracy\_plots.py" to visualise the accuracy every 200 iterations. The file "src/visualize/accuracy\_plots.py" consumes the "accuracy\_vs\_iter\_X.txt" files computed during the testing phase.
* Execute the file "src/visualisation/time\_plots.py" to visualise the time spent every 200 iterations. The file "src/visualize/time\_plots.py" consumes the "log.txt" files computed during the training phase. 
* Warning: the visualisation code assumes that we performed training for 5 different times using the default training parameters and we have data for all the scenarios "BSV", "ISK" and "NGA". 

### Description of the source code (with emphasis the CHESS scenarios)  ###

* The neural component ("src/networks/mnist_nets.py") has an output neuron for each cell/piece combination including the empty piece. 
Since we consider all possible pieces along with the empty cell (when no piece is on the cell), 
the neural component has 3x3x8 output neurons. 
We use o\_{i,j,p} to denote the output neuron associated with the (i,j) cell and the piece (or no piece) p, 
where p is in {e,bk,r,b,n,k,p,q} and e denotes no piece, bk is the black king, r is the white rook, 
b is the white bishop, n is the white knight, k is the white king, p is the white pawn and q is the white queen. 

* The AbstractTranslator objects ("src/abstract_translator.py") maintain the associations between neural outputs and abducible facts.

* The classes inside "src/chess/abduction" compute abductive proofs via calling the abduction engine "engine\abduction.pl" 
using the chess program "theories\chess.pl". The abductive proofs are computed based on the target of the abduction.

* In CHESS-BSV, the target of the abduction is *safe*, *draw*, or *mate*, so the abduction engine returns all board instances 
which represent either of these targets. In order to compute the abductive proofs, the class *ChessAbductionBSV* provides to the abduction engine a file named "input.pl" 
with contents of the form "input(scenario(1,Y,11), [ ])." with Y being either of *safe*, *draw*, or *mate*.
 
* In CHESS-ISK, the target of the abduction is *safe*, *draw*, or *mate* along with the coordinates of the cells that have pieces, so the abduction engine returns all possible board instances 
which represent either of these targets and which have pieces placed *only on the target coordinates*. In order to compute the abductive proofs, the class *ChessAbductionISK* provides to the abduction engine a file named "input.pl" 
with contents of the form "input(scenario(2,Y,21), [hard(at(\_,(X1,Y1))), hard(at(\_,(X2,Y2))), hard(at(\_,(X3,Y3)))])." with Y being either of *safe*, *draw*, or *mate* and (Xj,Yj) 
being the target coordinates. 

* In CHESS-NGA, the target of the abduction is *safe*, *draw*, or *mate* along with the coordinates of the cells that have pieces. 
The difference with CHESS-ISK is that in this scenario the target coordinates are not provided as part of the input but are
observed by the neural component. In particular, we ask the neural component to provide us with the (non-empty) piece it observes in each cell and 
we provide these cells to the abduction engine. We compute the neural observations using the method *computeNeuralObservations* inside
"src/train.py". We assume that the neural module observes the piece pk in the cell (i,j) if the output neuron 
o\_{i,j,pk} takes the maximum value among all output neurons o\_{i,j,pl}. 
In order to compute the abductive proofs, the class *ChessAbductionNGA* provides to the abduction engine a file named "input.pl" with contents of the form 
"input(scenario(3,Y,31), [soft(at(P1,(X1,Y1))), ..., soft(at(Pn,(Xn,Yn)))])." with Y being either of *safe*, *draw*, or *mate*, 
(Xj,Yj) being the coordinates of the non-empty cells and Pj being the pieces on those cells as have been observed by the neural module. 
A second difference with 
CHESS-ISK is that if the neural observations are not consistent with the target label (e.g., mate) or 
if they lead to an invalid board (see the "Assumptions" above for a description of the valid proofs), 
then the program returns proofs that differ as least as possible from the neural observations according to a cost function encoded in the chess program.   

* The returned proofs encode only the non-empty pieces assuming that the other cells are empty, so the classes inside "src/abduction" encode in the proofs that the other cells are empty. 

* In order to convert abductive formulas to arithmetic circuits we maintain the mappings from facts into literals in the arithmetic circuit. 
These mappings are stored in the *variable2Literal* dictionary. This dictionary is computed by the *Trainer* class from "src/train.py" and it is passed to the *abduce* method of the classes *ChessAbductionBSV*, *ChessAbductionISK*, *ChessAbductionNGA*. 

* The classes *ChessAbductionBSV*, *ChessAbductionISK*, *ChessAbductionNGA* use the *variable2Literal* dictionary to directly convert an abductive proof into an arithmetic circuit using PySDD. 

* The class representing arithmetic circuits is called SddNode and so the object named *sddnode* inside the method *train* from "src/train.py" represents 
the arithmetic circuit corresponding to the abductive proof. 

* The computation of WMC is done via traversing the arithmetic circuit. Arithmetic circuits are represented as trees and have four types of nodes: 
*decision*, *literal*, *true*, *false*. WMC is inductively computed as follows: if the current node is true, then return 1; if the current node is false, 
then return 0; if the current node is a positive literal, then return the weight of the literal (i.e., the weight of the output neuron associated with the litral); 
if the current node is a negative literal, then return 1 - the weight of the literal after ignoring negation; if the current node is a decision one,
then for each element of the form (A,B) sitting inside the node take the product A*B and then sum those products for all the elements sitting inside the node. 

* The computation of WMC is done in method *computeTensorWMC* defined in "src/loss.py". The first argument is the arithemic circuit corresponding to the abductive proof, 
the second is an SddManager (object for managing SddNode objects), the third is a mapping from literals in the arithemic circuit to output neurons 
(variable named *literal2OutputNeuron*) and the last argument is the weights of the output neurons.  For performance reasons we use a stack to traverse the nodes of the circuit in a DFS fashion. 

* Testing is done using the class inside "src/test.py". Testing proceeds as follows. First, we ask the neural component to provide us 
with the (non-empty) piece it observes in each cell (method *evaluate* inside class *Tester* from "src/test.py"). We assume that the neural component observes the piece pk in the cell (i,j) 
if the output neuron o\_{i,j,pk} takes the maximum value among all output neuron o\_{i,j,pl}. Then, we provide this information to an *Evaluator* object, line 31 in "src/test.py").  

* Given a testing example (*target*) and the neural observations (*facts*), the class *ChessBSV_NGA* returns true if the neural observations are consistent with the board status 
as in the testing example, e.g., the neural module observes pieces which represent a mate board. Otherwise, it returns false. 

* The class *ChessBSV_ISK * works similarly, however, there we additionally impose the contraint that the neural component must observe pieces only in the provided targets. 
This additional restriction is encoded in lines 45--46 in "src/chess/evaluation/chessISK.py". 

### Description of the training and testing data of the CHESS scenario ###

* The input chessboard is encoded as a list of MNIST digits, where each digit is associated with a chess piece or the empty one. 
The field *digit_images* represents the grid as a list of elements. The field *coordinates* encodes the positions of the non-empty cells (this information is only used in the CHESS-ISK scenario). Finally, the field label encodes the status of the board *safe* *draw*, or *mate*. 
We assume that the training and testing examples represent valid chess boards. 

