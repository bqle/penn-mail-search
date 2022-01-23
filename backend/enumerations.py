from enum import Enum

class School(Enum):
    COLLEGE_OF_ARTS_AND_SCIENCES = ['college of arts & sciences']
    ENGINEERING = ['engineering & applied science undergrad', 
                    'engineering & applied science masters',
                    'engineering & applied science phd'
                ]
    WHARTON = ['wharton undergraduate', 'wharton graduate']
    NURSING = ['nursing undergraduate']
    ANY = COLLEGE_OF_ARTS_AND_SCIENCES + ENGINEERING + WHARTON + NURSING
