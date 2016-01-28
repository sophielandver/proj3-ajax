Author: Sophie Landver

Path to project4 on ix: slandver@ix-trusty: ~/public_html/cis399/htbin/proj3-ajax

# proj3-ajax
Reimplementation the RUSA ACP controle time calculator with flask and ajax

## Brevet Terminology
- Information about what a brevet is and other useful terminology can be found at: http://www.rusa.org/faq1.html
- The rules for riders can be found at: http://www.rusa.org/brvreg.html
- Controles are checkpoints to which the rider must arrive and he/she must arrive to the checkpoint within a window of time. 
- "open time of a controle": the earliest time in which you can arrive to the controle
- "close time of a controle": the latest time in which you can arrive to the controle.
- "open duration of a controle": the start time plus the open duration is the earliest time in which you can arrive to the controle. 
- "close duration of a controle": the start time plus the close duration is the latest time in which you can arrive to the controle. 
- The first controle is always at distance 0 km. 

##Controle Time Calculation Rules
In these instruction I will often use the phrase "clean up steps" and by that I just mean a few simple steps that we take in order to turn a number into clear hours and minutes; I will show an example of these "clean up steps" in the example below. In addition, in the calculation time is rounded to the nearest minute; this will be shown in the clean up steps in the below calculation. 

Given a controle at distance D from the starting point, this is how you calculate the open duration, OD (again, once you have the open duration you simply add it to the start time of the brevet and then you obtain the open time of the controle):
Case 1: if D is zero, i.e. it is the first controle, then the OD is 00:00. DONE. 
Case 2: if D is greater than the brevet distance, then for the remainder of this calculation assume D = the brevet distance and continue on to Case 3. 
Case 3: To calculate the open duration of a controle at distance D we want to calculate what the earliest time at which someone can arrive to the controle is. Thus, to calculate the open duration we use maximum speeds (these are listed below). Now if the max speed was the same for all of the 1000 km, we would just do D/(max speed) and then a few clean up steps and then we would have our open duration. However, the max speed is not the same for all 1000 km and thus we often have to split up the calculation into a sum of quotients instead of just 1 quotient (and then of course do a few clean up steps). 
Here are the maximum speeds we use:
	- for the first 200 km of D, i.e 0<=km<= 200, the max speed is 34 km/hr
	- for the next 200 km of D, i.e. 200<km<=400, the max speed is 32 km/hr
	- for the next 200 km of D, i.e. 400<km<=600, the max speed is 30 km/hr
	- for the next 400 km of D, i.e. 600<km<=1000, the max speed is 28 km/hr

Example Calculation: Calculate the open duration of controls at 0 km, 100 km, 200 km, 399 km, 400 km, and 405 km of a 400 km brevet. 
1. open duration of controle at 0 km: This falls right into case 1 and thus the open duration, OD, is 00:00.
2. open duration of controle at 100 km: Since for the first 200 km the maximum speed is 34 km/hr, the maximum speed for the first 100 km is 34 km/hr. Thus, we do: 100/34 = 2.941... and (CLEAN UP STEPS) thus the whole number here is the number of hours so we have 2 hours and to figure out the minutes we do (2.941... - 2) * 60 = 56.470.. and lastly, we now round this number of minutes to the nearest minute giving us 56 minutes. Thus to get the number of minutes we subtracted the whole number and multiplied by 60. Thus we get 2 hours and 56 minutes, 02:56. 
3. open duration of controle at 200 km: From above we know that the max speed for the first 200 km is 34 km/hr. Thus we do 200/34=5.882... and (CLEAN UP STEPS) so we have 5 hours and for the number of minutes we have: (5.882.. - 5) *60 = 52.941.. and by rounding to the nearest minute we get 53 minutes. Thus we get 5 hours and 53 minutes, 05:53. 
4. open duration of controle at 399 km: From above we know that the max speed for the first 200 km of the 399 km is 34 km/hr. For the remaining 199 km (399-200) of the 399 km the max speed is 32 km/hr. Thus, the open duration is: 200/34 + 199/32 = 12.101.. and thus we get 12 hours and for minutes we have: (12.101.. - 12) * 60 = 6.066 --> 6 minutes. So we get 12 hours and 6 minutes, 12:06
5. open duration for 400 km: 200/34 + (400-200)/32 --> (clean up) --> 12:08
6. open duration for 405 km: this falls into case 2, thus D is now 400 km. Thus now the calculations are exactly the same as the calculations in #5 above. 

Given a controle at distance D from the starting point, this is how you calculate the close duration, CD:
Case 1: if D is zero, then the CD is 01:00 (this is just how it is set by rules). DONE. 
Case 2: if D is greater than or equal to the brevet distance than the CD is 13:30 for a 200 KM brevet, 20:00 for a 300 KM brevet, 27:00 for a 400 KM brevet, 40:00 for a 600 KM brevet, and 75:00 for a 1000 KM brevet. (again, this is just preset by the rules). DONE. 
Case 3: If you didn't fall into case 1 or 2, then to calculate the close duration for a controle at distance D this is what you do: We want to calculate the latest time at which someone can arrive to the controle. Thus we will use minimum speeds (these are listed below). Again just like with open duration, the minimum speed is not the same for the whole 1000 km and thus we often have to split up the calculation into a sum of quotients instead of just 1 quotient (and then of course do a few clean up steps). 
Here are the minimum speeds we use:
	- for the first 600 km of D, i.e 0<=km<= 600, the min speed is 15 km/hr
	- for the next 400 km of D, i.e. 600<km<=1000, the min speed is 11.428 km/hr

I will omit an example calculation for closing duration because the clean up steps and the way to split up the calculation into a sum of quotients have been shown in the open duration example problem. 




