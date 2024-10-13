pattern = """

What is Use Case?
Abbreviations and terms
Term
Description
Actor
Human or System Entity participating in a use-case
Goal
Use-case summary describing the desired outcome
HMI
Human-machine Interface
HMI Team
Team developing in-vehicle HMI
OC Team
Operational Concept team
SA Team
System Architecture team
TBD
to be defined
References
 
File Name 
Link
1
Use-Case Best Practices
https://www.cybermedian.com/the-nut-and-bolts-of-use-case-writing-best-practices-and-common-mistakes/
2
How to Write Good Use Case Names - 7 tips
https://tynerblain.com/blog/2007/01/22/how-to-write-good-use-case-names/
3
Alistair Cockburn. Writing Effective Use Cases
https://www-public.imtbs-tsp.eu/~gibson/Teaching/Teaching-ReadingMaterial/Cockburn00.pdf
4
OC UC. Lessons Learnt
https://evkama.sharepoint.com/:p:/r/sites/KamaEngineeringTeam/_layouts/15/Doc.aspx?sourcedoc=%7B86457B1A-FAD6-441F-B777-3ABA7F957A29%7D&file=OC%20Lessons%20Learnt.pptx&action=edit&mobileredirect=true
5
Use Cases in Theory and Practice
Use Cases in Theory and Practice. Alistair Cockburn.pdf



UC Template
All use-cases shall follow the template
    • Bold text: section title, should not be changed
    • Text in the angle brackets, template text, to be changed
Use-Case Title (Mandatory): "<Title>"
Goal (Maturity A, mandatory): <goal definition>
Context (Maturity A, optional): <execution environment>
Scope (Maturity A, optional): <design boundaries>
Actors (Maturity A, mandatory):
* Human (Mandatory)
  * <Human Actor 1>
* System (Optional)
  * <System Actor 1>
Preconditions (Maturity B, mandatory):
1. <Precondition 1
Triggers (Maturity B, mandatory):
1. <Trigger 1>
Main Scenario (Maturity C, mandatory):
1. <Action 1>
Post-conditions (Maturity B, optional):
1. <Post-condition 1>
Alternative Scenarios (Maturity C, optional):
1. <Branch 1>
Exceptions (Maturity C, optional):
1. <Exception 1>
Requirements (Maturity B, optional):
* <Requirement 1>
Mandatory sections
    • Mandatory section shall have meaningful section content
    • Mandatory section shall not have N/A text
    • Mandatory section shall 
Optional sections
    • List of the optional sections
    • Each optional section shall be marked with string (optional)
    • Each empty optional section shall be filled with N/A

UC Maturity
    • Level A: Title, Goal, Actors are provided and mandatory, Context, Scope are optional
    • Level B: Title, Goal, Actors, Preconditions, Triggers are provided and mandatory, Context, Scope, Post-conditions and Requirements are optional
    • Level C: Title, Goal, Actors, Preconditions, Triggers, Main Scenario are provided and mandatory, Context, Scope, Post-conditions, Requirements, Alternative Scenarios and Exceptions are optional
Actors
Human Actor is a non-exclusive role of a human participant.
    • Driver
    • Fleet Manager
    • Owner
    • Passenger
    • Pedestrian
    • User
    • Custom role
System
System Actors are the in-vehicle systems reflecting high-level operational abstraction.
In Vehicle
    • ADAS
    • AVAS 
    • Anti-theft System
    • Braking System
    • Drivetrain System
    • Exterior Light System
    • HUD
    • Interior Light System
    • Instrument Cluster
    • Passive Safety System
    • Wash and Wipe System
External
    • Cloud (general)
    • Mobile App
    • Widget
UC Requirements
    • is based on the Best Practices articles, see ref. 1, 2 and 3;
    • follows the Template structure above;
    • Applicable to the Description field of the use-case;
    • Each chapter is applicable to the corresponding chapter in the Description.
Use-Case Title (Mandatory)
    • Name is a string of <XXX> <YYY> <ZZZ> where
        ◦ XXX - verb infinitive
        ◦ YYY - descriptive noun
        ◦ ZZZ - optional predicate specifying use-case purpose
Examples
    • Calculate Speed
    • Calculate Vehicle Speed
    • Calculate Vehicle Speed from the road wheels
    • Calculate Vehicle Speed from braking system or motors
Goal (Maturity A, mandatory)
Goal is a free text, describing the author's point of view on the use-case implementation
    • what outcome is anticipated
    • which actor does the job
Is the source for the requirements, requirements must not confront the goal
Context (Maturity A, optional)
Context is a free text, describing the context where the use-case is modelled
    • time and place boundaries
    • environment conditions
    • ownership conditions
No information from this chapter can be considered as the requirements
Scope (Maturity A, mandatory)
Scope is a free text, describing the modelling boundaries for the use-case.
Actors (Maturity A, mandatory)
    • Actors shall list every use-case participant
    • No orphan Actors are allowed
Human (Mandatory)
    • Human actors represent distinct roles participating in a scenario
    • Business unit roles participating in scenario
System (Optional)
    • System Actors represent the In-Vehicle and External systems performing the actions
    • When it is not possible to identify the 
Preconditions (Maturity B, mandatory)
Preconditions is a semi-structured list describing the Actor states allowing use-case execution
    • The Precondition must form the Boolean statement
    • All Preconditions shall be TRUE to allow use-case execution
    • The Precondition may include the Boolean logic
        ◦ AND operand - both left and right parts are true
        ◦ OR operand - any left or right part is true
        ◦ NOT operand - next right part is negated
        ◦ brackets - combine inner conditions and operands into a single boolean value
    • User is Owner or Driver
    • Vehicle is (standstill and Driver presses braking pedal) or Gearbox in P position
Triggers (Maturity B, mandatory)
Triggers represent the events expected to happen to start the use-case execution
    • The Trigger us run by the Actor
    • The Triggers must form the Boolean statement
    • Any of the Triggers shall be TRUE to allow use-case execution
    • The Triggers may include the Boolean logic
        ◦ AND operand - both left and right parts are true
        ◦ OR operand - any left or right part is true
        ◦ NOT operand - next right part is negated
        ◦ brackets - combine inner conditions and operands into a single boolean value
    • Gearbox position changed to P or R
    • Vehicle speed is above 3kph
Main scenario (Maturity C, mandatory)
Describes the sunny-day case with the most optimistic execution path
    • Each step shall describe one of
        ◦ Human Actor
            ▪ provides information​
            ▪ receives information
            ▪ makes a choice​
        ◦ System Actor
            ▪ provides information​
            ▪ asks for information​
            ▪ does some work​
    • The Main Scenario shall have from 4 to 10 steps
    • Each step shall represent the finished action
Post-conditions (Maturity B, optional)
Post-condition is a semi-structured text of the expectations to be fulfilled on the Use-case end
    • The Post-condition must form the Boolean statement
    • All Post-conditions shall be TRUE to allow use-case execution
    • The precondition may include the Boolean logic
        ◦ AND operand - both left and right parts are true
        ◦ OR operand - any left or right part is true
        ◦ NOT operand - next right part is negated
        ◦ brackets - combine inner conditions and operands into a single boolean value
References
    • Main Scenario must match the Post-conditions on finish
    • Alternative Scenarios must match  the Post-conditions on finish
    • Exceptions may not match the Post-Conditions
Alternative Scenarios (Maturity C, optional)
The Alternative Scenario extends the Main Scenario rules and
    • Each entry must refer to a Main Scenario or other Alternative Scenario branch
    • Each entry must describe the logical branch alternative to the main scenario
    • Each entry must satisfy the Post-conditions
Exceptions (Maturity C, optional)
The Exceptions describe the known cases leading to non-satisfactory Post-conditions.
    • Each entry must refer to a single Main Scenario or Alternative Scenario
    • Each entry must include at least one Actor
    • Each entry must specify the alternative Post-conditions 
Requirements  (Maturity B, optional)
The requirements represent the non-functional requirements considered by the Main Scenario, Alternative Scenarios, Exceptions.
    • No orphaned requirements are allowed


"""