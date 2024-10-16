"""DATA"""
import pandas as pd

class DataIngestor:
    """DATA INIT"""
    
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.data_dict_init()
        self.question_best_init()
    def data_dict_init(self):
        """DICT INIT
        
        Dict structure: {
                question1: {
                    location1: {
                        stratification1: [index1, index2, ...],
                        stratification2: [index3, index4, ...],
                        ...
                        }
                    ...
                    }
                ...
                }
        """
        self.data_dict = {}
        for x in self.df.index:
            if self.df["Question"][x] not in self.data_dict:
                self.data_dict[self.df["Question"][x]] = {self.df["LocationDesc"][x]:
                                                          {self.df["Stratification1"][x]:[x]}}
            else:
                aux_dict = self.data_dict[self.df["Question"][x]]
                if self.df["LocationDesc"][x] not in aux_dict:
                    aux_dict[self.df["LocationDesc"][x]] =  {self.df["Stratification1"][x]:[x]}
                else:
                    aux_dict_strat = aux_dict[self.df["LocationDesc"][x]]
                    if self.df["Stratification1"][x] not in aux_dict_strat:
                        aux_dict_strat[self.df["Stratification1"][x]] = [x]
                    else:
                        aux_dict_strat[self.df["Stratification1"][x]].append(x)
    def question_best_init(self):
        """BEST QUESTION INIT"""
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]
        q1 = 'Percent of adults who achieve at least 150 minutes'
        q1 += 'a week of moderate-intensity aerobic physical activity or 75 minutes a week of '
        q1 += 'vigorous-intensity aerobic activity (or an equivalent combination)'
        q2 = 'Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
        q2 += 'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
        q2 += 'physical activity and engage in muscle-strengthening activities on 2 or more days '
        q2 += 'a week'
        q3 = 'Percent of adults who achieve at least 300 minutes a week of moderate-intensity '
        q3 += 'aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic '
        q3 += 'activity (or an equivalent combination)'
        q4 = 'Percent of adults who engage in muscle-strengthening activities on 2 or more '
        q4 += 'days a week'
        self.questions_best_is_max = [
            q1,
            q2,
            q3,
            q4,
        ]
