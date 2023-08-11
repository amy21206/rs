# Personalized-Parsons-Runestone
Develop Personalized Parsons Problem as Scaffolding for Code Writing on the Runestone System

To start, please run the requirements.txt

### Input:
* An incorrect solution to a programming problem (written by a student) - see `example_buggy_code.json`
* Basic Information of the write-code question itself - see `example_code_question_bank.xlsx`
  * `Problem Name`: Question Name 
  * Both Write-Code (`w_question_description`) & Parsons (`p_question_description`) question description
  * `Example_student_solution`: One representative student solution from the most common student solution cluster 
  * `Example_buggy_code`: One example student buggy solution from the previous student solution data
  * `Example_fixed_code`: One verified example personalized fixed solution written by the researcher
    * Verification: has higher similarity than the most common solution using [CodeBert](https://github.com/microsoft/CodeBERT) & [Fix-Explainer](https://github.com/yanamal/python_fix_explainer).
  * `Unittest_Code`: Unittest Code provided by Runestone system
  * `Default_Starting_Code`: Some write-code questions have default starting code for students to start from, we want to make sure the generated fixed solution has it
  * `Default_Test_Code`: Some write-code questions have default starting code for students to test, we want to remove it from the fixed solution
  * `Example_paired_distractor_correct`: The example correct line to pair with distractor
  * `Example_paired_distractor_wrong`: The example paired distractor generated by an expert
    

### Output:
A personalized Parsons problem in the Runestone format that is close to the incorrect input written solution.
```
-----
    class Cat: 
    =====
    class cat:  #paired
    =====
        def __init__(self, name, age): #settled
    =====
            self.name = name 
            self.age = age 
    =====
            self.name == name 
            self.age = age  #paired
    =====
        def __str__(self): 
    =====
        def __str__:  #paired
    =====
            return "name: " + self.name + ", age: " + str(self.age) #settled
    =====
        def make_sound(self): 
    =====
        def make_sound():  #paired
    =====
            return 'Meow'
```

A good entry point is [entry_point.py](https://github.com/xinyinghou/personalized-parsons-runestone/blob/main/entry_point.py): it's an end-to-end example of how the system is designed to work.


### ToDo
- [X] Test on the current Runestone webpage interface
- [X] Add a requirement file
- [ ] Connect with Zihan's runestone interface to do evaluation