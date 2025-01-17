# Personalized-Parsons-Runestone
Develop Personalized Parsons Problem as Scaffolding for Code Writing on the Runestone System

To start, please run the `requirements.txt`

### Static Files:
* `Classroom_Evaluation_Material.csv` - Nested Dict file for the classroom study
* `personalized_solution_cache.db` - stored 290 personalized solutions of past student buggy code


### Input:
* An incorrect solution to a programming problem (written by a student) - see `example_buggy_code.json`
* Basic Information of the write-code question itself - see `example_code_question_bank.xlsx`
  * `Problem Name`: Question Name 
  * Write-Code (`w_question_description`) question description
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
    Finish the function ``less_dict`` below which takes a dictionary ``d`` and an
    integer ``cutoff`` and returns a new dictionary that contains only the key-value
    pairs where the value is less than the cutoff. For example, ``less_dict({'a':
    20, 'b': 10}, 15)`` returns ``{'b': 10}``, ``less_dict({'a': 30, 'b': 20}, 40)``
    should return ``{'a': 30, 'b': 20}``, ``less_dict({'a': 20, 'b': 10}, 5)``
    should return ``{}``.
    -----
    def less_dict(d, cutoff): 
    =====
    def less_dict(c, cutoff): #paired
    =====
        d2 = {} 
        for k in d: #settled
    =====
            if d[k] < cutoff: 
    =====
            if d[k] <= cutoff: #paired
    =====
                d2[k] = d[k] 
    =====
                d2[k] = cutoff #paired
    =====
        return d2 #settled
```

A good entry point is [entry_point.py](https://github.com/xinyinghou/personalized-parsons-runestone/blob/main/entry_point.py): it's an end-to-end example of how the system is designed to work.


### ToDo
- [X] Test on the current Runestone webpage interface
- [X] Add a requirement file
- [ ] Connect with Zihan's runestone interface to do evaluation
