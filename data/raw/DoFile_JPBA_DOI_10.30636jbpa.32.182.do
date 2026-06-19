/// ***************************************** ///
/// Data Cleaning and Analysis File for:      ///
/// DOI_10.30636/jbpa.32.182 using dataset:   ///
/// Dataset_JBPA_DOI_10.30636/jbpa.32.182.dta ///
/// Author: Ulrich Thy Jensen. July 2020      ///
/// ***************************************** ///

/* Initial Screening of Respondents:
    (1) Removing respondents with missing values on experimental conditions
	(2) Removing respondents who don't meet inclusion criteria of adult living 
	in the US using VPN/VPS detection and IP addresses */

gen missing = 0

replace missing = 1 if soc_dist_DQ != .

replace missing = 1 if soc_dist_CM != .	
	
tab1 missing ipblock outsideus

drop if missing == 0 & ipblock == 1 | missing == 0 & outsideus == 1 
 /* 140 respondents excluded */ 

tab missing

drop if missing == 0
 /* 98 respondents with missing values on exp condition excluded */


/* Covariates for Descriptive Statistics, Correlation Matrix & Balancing */

/* Dummy variable for DQ social distance */

tab soc_dist_DQ

gen soc_dist_DQ_dum = .

replace soc_dist_DQ_dum = 0 if soc_dist_DQ == 4

replace soc_dist_DQ_dum = 1 if soc_dist_DQ == 1 | soc_dist_DQ == 2 ///
 | soc_dist_DQ == 3

/* Gender: Male 0 Female 1 */

tab gender

gen female_dum = .

replace female_dum = 1 if gender == 2

replace female_dum = 0 if gender == 1

tab female_dum

/* Age */

tab byear

gen age = 17+byear

sum age

/* Education

1 "Less than high school"
2 "High school graduate"
3 "Some college"
4 "2-year degree"
5 "4-year degree"
6 "Professional degree"
7 "Doctorate"

*/

tab education

/* Race 

1 "African American or Black" RECODE NEW VALUE: 2
2 "Asian American or Asian" RECODE NEW VALUE: 3
3 "Hispanic or Latino/Latina/Latinx" RECODE NEW VALUE: 4
4 "Middle Eastern or Arab" RECODE NEW VALUE: 6
5 "Multiracial" RECODE NEW VALUE: 7
6 "Pacific Islander" RECODE NEW VALUE: 8
7 "White or Caucasian" RECODE NEW VALUE: 1
8 "Other/Self-identify (text optional)" RECODE NEW VALUE: 9
9 "American Indian/Native American" RECODE NEW VALUE: 5

*/

recode race_aa (1=2)
recode race_asian (1=3)
recode race_hisp (1=4)
recode race_meast (1=6)
recode race_multi (1=7)
recode race_island (1=8)
recode race_ident (1=9)
recode race_nat (1=5)

gen race = max(race_aa, race_asian, race_hisp, race_meast ///
 , race_multi, race_island, race_white, race_ident, race_nat)

tab race

gen white_dum = .

replace white_dum = 0 if race == 2
replace white_dum = 0 if race == 3
replace white_dum = 0 if race == 4
replace white_dum = 0 if race == 5
replace white_dum = 0 if race == 6
replace white_dum = 0 if race == 7
replace white_dum = 0 if race == 8
replace white_dum = 0 if race == 9

replace white_dum = 1 if race == 1

tab white, m

/* Political Ideological Orientation: Indicator */

tab pol_ideo

gen lib_dum = . /* Indicator: Lib 1; Conservative 0 */

replace lib_dum = 1 if pol_ideo == 1 | pol_ideo == 2 | pol_ideo == 3

replace lib_dum = 0 if pol_ideo == 5 | pol_ideo == 6 | pol_ideo == 7

tab lib_dum

/* Short Cognitive Mental Ability Test Score */

/* 1. Q: The ages of Mark and Adam add up to 28 years total. ///
 Mark is 20 years older than Adam. How many years old is Adam?. A = 4 */

tab numreason1
 
gen cog_1_corr = 0

replace cog_1_corr = 1 if numreason1 == 4

tab cog_1_corr

/* 2. Q: If it takes 10 seconds for 10 printers to print out 10 pages ///
 of paper, how many seconds will it take 50 printers to print out ///
 50 pages of paper?. A = 10 */

tab numreason2

gen cog_2_corr = 0

replace cog_2_corr = 1 if numreason2 == 10

tab cog_2_corr

/* 3. Q: On a loaf of bread, there is a patch of mold. ///
 Every day, the patch doubles in size. If it takes 40 days for the patch ///
 to over the entire loaf of bread, how many days would it take for ///
 the patch to cover half of the loaf of bread? . A = 39 */

tab numreason3

gen cog_3_corr = 0

replace cog_3_corr = 1 if numreason3 == 39

tab cog_3_corr
 
/* # Correct Answers */

egen cogn_no = anycount(cog_1_corr cog_2_corr cog_3_corr), values(1)
 
tab cogn_no 
 
/* Big 5 Personality Inventory */

/* Extraversion 

bfi_36 "Is outgoing, sociable"
bfi_1 "Is talkative"
bfi_26 "Has an assertive personality"
bfi_16 "Generates a lot of enthusiam"
bfi_11 "Is full of energy"
bfi_6 "Is reserved" - NB REVERSE
bfi_31 "Is sometimes shy, inhibited" - NB REVERSE
bfi_21 "Tends to be quiet - NB REVERSE 

*/

recode bfi_6 (1=5) (2=4) (3=3)
 
recode bfi_31 (1=5) (2=4) (3=3)

recode bfi_21 (1=5) (2=4) (3=3) 

gen extraversion = ((bfi_36+bfi_1+bfi_26+bfi_16+ ///
 bfi_11+bfi_6+bfi_31+bfi_21)-8)/32*100
 
sum extraversion 
 
/* Agreeableness

bfi_32 "Is considerate and kind to almost everyone"
bfi_42 "Likes to cooperate with others"
bfi_7 "Is helpful and unselfish with others"
bfi_17 "Has a forgiving nature"
bfi_22 "Is generally trusting"
bfi_2 "Tends to find fault with others" - NB REVERSE
bfi_12 "Starts quarrels with others" - NB REVERSE
bfi_27 "Can be cold and aloof" - NB REVERSE
bfi_37 "Is sometimes rude to others" - NB REVERSE 

*/
 
recode bfi_2 (1=5) (2=4) (3=3)
 
recode bfi_12 (1=5) (2=4) (3=3)
 
recode bfi_27 (1=5) (2=4) (3=3)
 
recode bfi_37 (1=5) (2=4) (3=3)

gen agreeable = ((bfi_32+bfi_42+bfi_7+bfi_17+ ///
 bfi_22+bfi_2+bfi_12+bfi_27+bfi_37)-9)/36*100 
 
sum agreeable 

/* Conscientiousness

bfi_3 "Does a thorough job"
bfi_33 "Does things efficiently"
bfi_38 "Makes plans, follows through with them"
bfi_13 "Is a reliable worker"
bfi_28 "Perseveres until the task is finished"
bfi_43 "Is easily distracted" - NB REVERSE
bfi_8 "Can be somewhat careless" - NB REVERSE
bfi_23 "Tends to be lazy" - NB REVERSE
bfi_18 "Tends to be disorganized" - NB REVERSE

*/

recode bfi_43 (1=5) (2=4) (3=3)
 
recode bfi_8 (1=5) (2=4) (3=3)
 
recode bfi_23 (1=5) (2=4) (3=3)
 
recode bfi_18 (1=5) (2=4) (3=3)

gen conscient = ((bfi_3+bfi_33+bfi_38+ ///
 bfi_13+bfi_28+bfi_43+bfi_8+bfi_23+bfi_18)-9)/36*100

sum conscient

/* Neuroticism

bfi_19 "Worries a lot"
bfi_14 "Can be tense"
bfi_39 "Gets nervous easily"
bfi_4 "Is depressed, blue"
bfi_29 "Can be moody"
bfi_34 "Remains calm in tense situations" - NB REVERSE
bfi_24 "Is emotionally stable, not easily upset" - NB REVERSE
bfi_9 "Is relaxed, handles stress well" - NB REVERSE

*/

recode bfi_34 (1=5) (2=4) (3=3)
 
recode bfi_24 (1=5) (2=4) (3=3)
 
recode bfi_9 (1=5) (2=4) (3=3)

gen neurotic = ((bfi_19+bfi_14+bfi_39+bfi_4+ ///
 bfi_29+bfi_34+bfi_24+bfi_9)-8)/32*100

sum neurotic

/* Openness

bfi_25 "Is inventive"
bfi_5 "Is original, comes up with new ideas"
bfi_30 "Values artistic, aesthetic experiences"
bfi_20 "Has an active imagination"
bfi_40 "Likes to reflect, play with ideas"
bfi_44 "Is sophisticated in art, music, or literature"
bfi_10 "Is curious about many different things"
bfi_35 "Prefers work that is routine" - NB REVERSE
bfi_41 "Has few artistic interests" - NB REVERSE

*/

recode bfi_35 (1=5) (2=4) (3=3)
 
recode bfi_41 (1=5) (2=4) (3=3)

gen open = ((bfi_25+bfi_5+bfi_30+bfi_20+bfi_40+ ///
 bfi_44+bfi_10+bfi_35+bfi_41)-10)/40*100
 
sum open 

 
/* Descriptive Statistics: Reported in Appendix A, Table A1 */
  
sum true_dice_DQ true_dice_CM soc_dist_DQ_dum soc_dist_CM ///
 i.female_dum age hhinc i.white i.education ibn.education ///
 i.lib_dum cogn_no extraversion agreeable conscient neurotic ///
 open
 /* All respondents */
  
gen group_sst = . 
 /* Dummy for exp condition: 0 "DQ", 1 "CM" */

replace group_sst = 0 if true_dice_DQ != . & soc_dist_DQ_dum != .   

replace group_sst = 1 if true_dice_CM != . & soc_dist_CM != .   
  
sort group_sst

by group_sst: sum true_dice_DQ true_dice_CM soc_dist_DQ_dum soc_dist_CM ///
 i.female_dum age hhinc i.white i.education ibn.education ///
 i.lib_dum cogn_no extraversion agreeable conscient neurotic ///
 open 
 /* Respondents by exp condition */
 
/* F-tests for Balancing on Covariates Across Exp Conditions:
    Reported in Appendix A, Table A1 */
 
anova group_sst i.female_dum 

anova group_sst c.age

anova group_sst hhinc 

anova group_sst i.white

anova group_sst education

anova group_sst i.lib_dum

anova group_sst c.cogn_no
 
anova group_sst c.extraversion
  
anova group_sst c.agreeable

anova group_sst c.conscient

anova group_sst c.neurotic

anova group_sst c.open

anova group_sst i.female_dum c.age c.hhinc i.white education ///
 i.lib_dum c.cogn_no c.extraversion c.agreeable ///
 c.conscient c.neurotic c.open
 
regress

testparm i.female_dum c.age c.hhinc i.white i.education ///
 i.lib_dum c.cogn_no c.extraversion c.agreeable ///
 c.conscient c.neurotic c.open 
 /* No joint group mean difference in covariates across exp conditions.
    Not reported in article */

/* Generate Variables for Number of Wins and Cheat Rates 
    based Dice Prediction Game */

egen no_win_40 = anycount(r1_predictout r2_predictout r3_predictout ///
 r4_predictout r5_predictout r6_predictout r7_predictout r8_predictout ///
 r9_predictout r10_predictout r11_predictout r12_predictout r13_predictout ///
 r14_predictout r15_predictout r16_predictout r17_predictout r18_predictout ///
 r19_predictout r20_predictout r21_predictout r22_predictout r23_predictout ///
 r24_predictout r25_predictout r26_predictout r27_predictout r28_predictout ///
 r29_predictout r30_predictout r31_predictout r32_predictout r33_predictout ///
 r34_predictout r35_predictout r36_predictout r37_predictout r38_predictout ///
 r39_predictout r40_predictout), values(1)

gen cheat_rate = (6/5)*((no_win_40/40)-(1/6)) 
 /* Using transformation in Olsen et al. JPART. 2019 Footnote 11 */ 
 
sum cheat_rate
 /* 0.43 (SD = 0.38) -.2:1 ; 
 Comparable to Olsen JPART 0.38 (SD = 0.38) -0.14:1 */
	
/* Prevalence Estimates of Dishonest Behavior: Reported in Figure 1 */

sum true_dice_DQ, d
 /* Prevalence estimate of dishonest behavior when asked directly */

display .3413233/sqrt(536)
 /* Sampling variance */	

tab true_dice_CM

display ((201/523)+(2/12)-1)/(2*(2/12)-1)
 /* Prevalence estimate of dishonest behavior when using crosswise model.
    Estimate calculated using formula by Höglingler and Jann (2018, 9) as shown
	in article */
	
display sqrt((((201/523)*(1-(201/523)))/(((523)*((2*(2/12)-1)^2)))))	
 /* Sampling variance calculated using formula by Jann et al. 2012 as shown
    in article */

display .03190544*sqrt(523)
 /* SD for Z test below */	
 
/* Test for difference in prevalence estimates in dishonest behavior : 
 Two sided two-sammple z tes for equality of means */ 

/// ztesti n1 x1 sd1 n2 x2 sd2 ///

ztesti 536 .8656716 .3413233 523 .673518164 .72965167


/* Distribution of Observed # of Wins: Reported in Figure 2 */

tab no_win_40


/* Prevalence Estimates of Social Distancing: Reported in Figure 3 */
 
sum soc_dist_DQ_dum, d 
 /* Prevalence estimate of social distancing behavior when asked directly */
 
display .4596572/sqrt(536)
 /* Sampling variance */ 
 
tab soc_dist_CM 
 
display ((307/523)+(2/12)-1)/(2*(2/12)-1)
 /* Prevalence estimate of social distancing behavior when using crosswise 
    model. Estimate calculated using formula by Höglingler and Jann (2018, 9) 
	as shown in article */ 
 
display sqrt((((307/523)*(1-(307/523)))/(((523)*((2*(2/12)-1)^2)))))	
 /* Sampling variance calculated using formula by Jann et al. 2012 as shown
    in article */
	
display .03229496*sqrt(523)
 /* SD for Z test below */	
 
/* Test for difference in prevalence estimates in social distancing behavior : 
 Two sided two-sammple z tes for equality of means */ 

/// ztesti n1 x1 sd1 n2 x2 sd2 ///
 
ztesti 536 .3022388 .4596572 523 .369502868 .73855968 


/* Correlation between self-reported Willingness to Social Distance measures
 whether respondents indicated that have previously practiced social
 distancing: Correlations reported in "Discussion and Conclusion" section */

tab soc_dist_DQ

recode soc_dist_DQ (1=0) (2=0) (3=0) (4=1)

sum soc_dist1-soc_dist7, d

pwcorr soc_dist_DQ soc_dist1 soc_dist2 soc_dist3 soc_dist4 soc_dist5 ///
 soc_dist6 soc_dist7, star(0.001)
