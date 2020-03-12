# ODI_result_predictor
Now-a-days Cricket is one of the most watched game after Soccer. Winning of cricket match depends on various factors like home advantage, past performances, experience in the match, performance at the specific venue, performance against the specific team and the current form of the team and the player. In this current project we are fetching all the data for previous matches and we are mainly focusing on building our model based on the performance of the team at a particular stadium and obviously we will be comparing the past performances of both the teams and will be giving weightage to individual player performances. For that we are going to use real time data that has never been used for this particular problem.  In past few years, lot of work and research papers have been published which measure only player performance and winning predictions. We want to make a total score based on batsman and bowler for each team and compare it respectively from opponent team for predicting the winner of the match. As One-Day International (ODI) games rise in popularity, it is important to understand the possible predictors that affect the game outcome and with the use of machine learning and statistics we are trying to predict the result at better accuracy. Information Mining and Machine learning in Sports Analytics, is a fresh out of the box new research field in Computer Science with a ton of test.

Data has been collected from different websites through python web scraping. 
• List of matches with their winner and stadium details. 
• Playing squad of the teams and their stats till match date. 
During runtime we will collect data on following attributes. 
• Playing XI of the teams. • Ongoing/upcoming ODI matches. 

For player to qualify as batsman or bowler and checking the strength of individuals in bowling and batting department we are using the following constraints.

Batsman Threshold = 25 (if bat_score <= 25, we are not considering the player as a batsman)

Batsman Score = sqrt(inn/match)*(0.6(avg/runs/100*100s+50*50s)))+0.4*SR LIMITATION:-        If(no. of 100’s = no. of 50’s = 0)                                   Then(100*100s+50*50s = highest score of that batsman) 

Bowler Threshold = 8 (if bowl_score <= 8, we are not considering the player as a bowler) 

Bowler Score = sqrt(inn/match)*((100-(avg+SR)+(10*5w)/inn)/econ) 

first update_data.py is run to update the data till the time.

then, main.py file is run to predict the result before the beginning of matches.(after the squad of teams are revealed on website)

At first, we are fetching the data of list of matches from website with variable years because the prediction could change for certain teams for data being taken for certain period of time so we wish to check our prediction for variable matches data.
Then trying to collect the details of playing xi for the both teams but in case that information is not available we are using last squad details for each team to collect the details of bowlers and batsman of each teams.
We are collecting the list of upcoming/ongoing ODI matches and displaying it so that user can choose the match they wish to see the prediction details, and with all data being collected from website from team’s name to stadium name we are using them to sort the data for those teams.
Prediction implementation yet to be done and we wish to do that in remaining time.

prediction accuracy

![pred1](https://github.com/sannu01/ODI_result_predictor/blob/master/output/random.png)

user interface


![pred](https://github.com/sannu01/ODI_result_predictor/blob/master/output/Screenshot%20(5).png)






 
 
