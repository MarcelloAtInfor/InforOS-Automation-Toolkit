# AES (Application Event System) Knowledge Base

> Auto-generated from AES Guide PDF using extract_aes_guide.py
> Source: AES_Guide.pdf (212 pages)

## Table of Contents

1. [Overview](#overview)
2. [Event Types](#event-types)
3. [Event Handler Configuration](#event-handler-configuration)
4. [Action Types](#action-types)
5. [Expression Syntax](#expression-syntax)
6. [Suspension & InWorkflow Pattern](#suspension--inworkflow-pattern)
7. [Scenario Walkthroughs](#scenario-walkthroughs)
8. [Full Chapter Extraction](#full-chapter-extraction)

---

## Overview

The Application Event System (AES) in SyteLine/CSI provides an event-driven framework for automating business processes. Events are triggered by IDO operations (insert, update, delete, load) and can execute chains of actions including variable assignment, conditional logic, method calls, email notifications, and ION workflow integration.

### Key Concepts

- **Events**: Named triggers fired by IDO operations (e.g., `IdoOnItemUpdate`)
- **Event Handlers**: Named configurations attached to events, with conditions and ordered actions
- **Event Actions**: Individual steps within a handler (SetVariable, CallWorkflow, RaiseError, etc.)
- **Expressions**: Formula language used in conditions and action parameters (`EXPR()`, `GETVALUE()`, etc.)
- **Suspension**: Mechanism for pausing handler execution during async operations (ION workflows)

---

## Event Types

*From Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31 (page 4):*

The Framework Event Service . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Setting up the Framework Event Service . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Processing order in the Framework Event Service  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Administrative details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28
Events and event handler revisions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28
Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31

About the Access As identifier . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31
About events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .32
About event triggers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .34
About event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .36
About event actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .37
About event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .38
About event action parameter forms  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .40
About event variables and initial states  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .41
About event global constants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .42

Setting up custom events and handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .45
Designing a custom event  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .46
About event handling and order . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .47
Determining names of IDO collections and components . . . . . . . . . . . . . . . . . . . . . . . . . . . .48
Refreshing the metadata cache . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .50
Chapter 4: Tracking Event System Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Handler Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Queue form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Revisions form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55
Event Handler Revisions form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55

*From Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57 (page 5):*

Framework events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .122
Application events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .125
Event action types  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Expressions and functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Pre-parser functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .127
Expression operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .128
Appendix C: Expression Grammar  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Restrictions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Start symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Character sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133

*From Chapter 2: How the Application Event (page 13):*

includes some framework events as part of the system. Infor does not include handlers for these 
events. These events were created to provide events that other developers can use with their own 
custom event handlers. 
When events can be generated 
An application event can be generated when: 
z
A system user performs a particular action, perhaps only on a given form and/or when a particular 
business process is involved. 
z
A database calculation is performed, perhaps resulting in a certain value. 
z
Another event results in generating this event. 
z
A certain amount of time has passed. 
These are all examples of situations and conditions that can fire events: 
z
A sales representative saves a record in the Customers form. 
z
A manager changes the credit hold status of a customer. 
z
A factory manager adds a new item to the list of those being manufactured in that facility.

z
The first day of each month arrives. (An event can be used to generate a monthly report, for 
instance.) 
z
The quantity-on-hand of a particular item becomes less than zero. 
Where events can be generated 

z
In the client tier, the event can be generated by using a form that has a form event handler with a 
response type of Generate Application Event. 
z
In the middle tier, the event can be generated by invoking an appropriate .NET method. 
z
In the database tier, the event can be generated by using an appropriate stored procedure. 
z
In any tier, an event can generate another event by using the GenerateEvent action type. 
For details on how to generate an event from any of these locations, see “Firing events” on page 120. 
Controlling the sequence of event handlers and 
actions 
Two types of settings control the order in which event handlers and their actions execute: 
z
Each event handler has a handler sequence number. Handlers execute in the order of their 
sequence numbers. 
To modify the flow and change handler sequence order, use the Keep With and Chronology 
options on the Event Handlers form or the Event Handler Sequence form. 
See “About event handling and order” on page 47. 
z
The event actions associated with each event handler also have their own action sequence 
numbers. These execute in numeric order, unless: 
z
You use the Initial Action option on the Event Handlers form to designate that a particular 
action should execute first. 
z
You use certain event action types to modify the flow. 
See “About event actions” on page 37. 
Restricting which handlers run 
There might be times when you want or need to disable the event handlers created by one or more 
development organizations, including yours, at least temporarily. This would occur typically when you

are troubleshooting problems with the application event system. The system offers two basic ways to 
disable event handlers. 
Using event handler settings 
When you want to disable only certain event handlers temporarily, use the Active check box on the 
Event Handlers form. 
You can only disable (or enable) event handlers that have the same Access As identifier that you 
have. You cannot, for instance, use this technique to disable Core event handlers. 
Using the Session Access As form 
When you want to disable (or enable) all the event handlers created by a particular developing 
organization all at once, you can use the Session Access As form to accomplish this. 
Note: An alternate way to accomplish the same thing for individual handlers with your Access As 
value is to open the Event Handler form and for each event handler that you do not want to include in 
testing or debugging, clear the Active check box. 
An example 
Suppose, for example, that a customer is having a problem that he suspects is being caused by 
something he did in the event system, but he is not sure what. He places a call to Infor technical 
support, and the technical support representative wants to verify that the customer’s custom event 
handlers are not causing the problem. 
In this case, the technical support representative might ask the customer to temporarily disable all 
custom event handlers so that the operation can be tested with only standard functionality in place. 
The technical support representative might instruct the customer to use the Session Access As form 
to perform either of these actions: 
z
In the Include Access As field, specify Core,BaseAppAccessAs where BaseAppAccessAs is 
the Access As identifier associated with the base application installed on the system. 
With this setting, only the Infor core (framework) and base application event handlers will execute. 
Custom event handlers created by the end-customer do not execute. 
See “Session Access As form options” on page 16. 
z
Leave the Exclude Access As field blank, and select the Exclude Blank Access As check box. 
This option allows all Infor and business partners event handlers to operate. Only the customer’s 
event handlers are ignored. 
See “Session Access As form options” on page 16.

Session Access As form options 
To disable or enable event handlers using the Session Access As form, use any of these options: 
Note: You are not obligated to use both the Include Access As and the Exclude Access As fields. 
You can use any combination of the options available on this form. 
z

*From Chapter 3: Designing and Using Events (page 31):*

Event types 
Events can be one of three general types: 
z
Core, or framework, events – These are events that Infor has defined and built in to the system. 
They are tagged with an Access As identifier of Core. 
These events generally fall into one of two categories: 
z
IDO (business process-related) events that are generated when certain IDOs are invoked. 
These IDOs include IdoOnItemInsert, IdoOnLoadCollection, IdoOnInvoke, and others. You 
can identify these events easily by their names, which begin with the letters Ido. 
z
Session events that are generated when certain session activities take place. 
These include SessionOnLogin, SessionOnLogout, and SessionOnVarChanged. 
These events are always synchronous and transactional. Some can be optionally suspended to 
await user responses.

z
Application-specific events – These are events that typically have been created by Infor, its 
business partners, and authorized vendors. They are tagged with an Access As identifier that 
indicates what application or development organization they belong to. 
z
Customer-defined events – These are events that a developer in an end-customer organization 
has created. They are tagged with a blank Access As identifier, which indicates that they were 
created by and belong to the customer. 
See “About the Access As identifier” on page 31. 
Defining events 
Events can be defined (named) on these forms: 
z
Events 
z
Event Triggers 
z
Event Handlers 
To define an event, specify the name of the event in the Event Name field of one of these forms.
Note: If you do not name the event on the Events form, it is still available to the drop-down lists on 
other forms. Events named on those forms, however, do not display on the Events form. So, if you 
want the event to display on the Events form, you should name the event on that form. 
When an event is defined, or named, it is really just that: a name. Until you define a way for it to be 
triggered or initiated, the event remains just a name. This can be done using either the Event 
Triggers form, the Event Handlers form, or both. 
See “About event triggers” on page 34. 
For more information about any of these forms, see the online help for that form. 
Modifying events 
Once an event has been created and saved, the only thing you can modify is the event's description. 
The event name and other attributes are locked. 
Note: You can modify an event's description only if the Access As field has the value of the current 
Access As value, as displayed on the Access As form. 
To modify an event's description: 

Open the Events form and select the event you want to modify. 

In the Description field, modify the description text as desired. 

Save. 
Deleting events 
If you are certain you no longer need an event and you want to delete it, you can.

You can delete an event only if the Access As field has the value of the current Access As value, as 
displayed on the Access As form. 
To delete an event: 

Open the Events form and select the event you want to delete. 

From the Actions menu, select Delete. 

Save. 
About event triggers 
An event trigger is defined as a condition that causes a particular event to fire, more-or-less 
independent of anything that might be happening in the user interface. The event trigger carries a set 
of event trigger parameters for use when the event fires. 
An event trigger can be set to fire the event only once, or it can be set to retest for its condition after 
waiting a certain amount of time since either of these situations was true: 
z
The trigger last successfully fired the event. 
z
The trigger last tested unsuccessfully for its condition. 
In both cases, you can set the interval for the event trigger to wait, both for the successful firing of the 
trigger and for the unsuccessful test for the trigger conditions (using separate settings). Testing and 
retesting is accomplished by means of polling; this is not a true interruptive trigger. 
An event trigger carries with it the user name and configuration in effect at the time it was defined. 
This data is passed on to the event state when the trigger fires the event. 
Defining event triggers 
Event triggers are defined using the Event Triggers form. Use this form to determine the condition 
that will fire the event, set the parameters to be passed to the event when it fires, and specify retest 
intervals. 
To create an event trigger: 

Open the Event Triggers form. 

Press F3. 

From the Actions menu, select New. 

From the Event Name drop-down list, select the event for which you want to define a trigger. 
Note: You cannot define a trigger for a framework (Core) event. 

On the Trigger tab, in the Condition field, specify the condition at which the event is to fire. 
See “Triggers and conditions” on page 35.

On the Parameters tab, specify the name and values for any event parameters for which you 

*From Appendix A: Sample Scenarios (page 67):*

added. In this example, you do not need to create an event, because Infor provides an event named 
IdoPostItemInsert that you can use. All you need to do is create an event handler for that event and 
assign an action to it that generates and sends the message to the system administrator. 
We could use the IdoOnItemInsert framework event instead of the IdoPostItemInsert event. This will 
be significant when we get to the section on  Refining the message on page 71. The advantage of 
using the IdoPostItemInsert event is that, if you allow the Users form to auto-assign the user ID 
number (instead of specifying the user ID number yourself), the system waits until the ID number has 
been assigned before filling in the "CustNum" data in the message. If we use the IdoOnItemInsert 
event, the system does not wait, which means that, if you auto-assign the customer ID number, the 
restulting message has "TBD" in place of the actual customer number. 
To set this up: 
1.
Create the event handler: 
a.
Open the Event Handlers form. 
b.
Press F3. 
c.
Press Ctrl+N. 
d.
Create the handler with these settings:  
Field or Option 
Setting / Comments 
Event Name 
From the drop-down list, select IdoPostItemInsert. 
Note: For details about this and the other 
framework events included with the system, see 
“Framework events” on page 122. 
Applies to Initiators 
Leave blank. 
Applies to Objects 
Specify SLCustomers. 
To determine what object you need, see the 
procedure provided in the online help for this field. 
Keep With 
Leave blank. 
Chronology 
Leave blank. 
Ignore Failure 
Cleared. 
Suspend 
Cleared.

For more information about any of these fields and options, see the help for the Event 
Handlers form. 
e.
Save. 
2.
Define the action for the event handler you just created: 
a.
In the Event Handlers form, select the handler you created in Step 1. 
b.
Click Event Actions. 
c.
In the Event Actions form, in the Action Sequence field, specify 10. 
d.
From the Action Type drop-down list, select Notify. 
e.
Click Edit Parameters. 
f.
In the Event Action Notify form, click the To button. 
g.
In the Event Action Parameter Recipients form, from the list of recipients, select the user ID 
of the credit manager (or whoever is serving in that role).  
h.
Click Update and then OK. 
i.
In the Subject field, specify New Customer! 
j.
In the Category field, specify Change Notification.
k.
In the Body field, specify We have a new customer! 
Synchronous 
Cleared. 
Because this notification does not require any 
response from the credit manager, it can run 
asynchronously. For more information, see 
“Synchronicity” on page 16. 
Active 
Selected. 
Can Override 
Selected. 
Transactional 
Cleared. 
Obsolete 
Cleared. 
Initial State 
Leave blank. 
Initial Action 
Leave blank. 
Note: Technically, you can specify any integer you want in this field, and the 
system treats them sequential order. We recommend using multiples of ten, 
initially at least, just in case you later need to add more action steps between 
existing steps, so you do not need to renumber all existing steps. 
TIP: You can select more than one recipient. Also, to deselect a recipient, click 
the user ID again. 
Field or Option 
Setting / Comments

l.

*From Appendix B: Reference Tables (page 119):*

Framework events 
z
Application events 
z
Event action types 
z
Event action parameters 
z
Expressions and functions 
z
Expression operators

Firing events 
This table provides details about: 
z
Where events can be generated from (Tier) 
z
What can be used to generate them from that location (Triggered by) 
z
How to set them up (Details for construction) 
z
Whether the event is generated as a synchronous or asynchronous event (Synchronous?) 
Tier 
Triggered by 
Details for construction 
Synchronous? 
Client 
Event handler in 
form 
Use a response type of Generate 
Application Event, select the Synchronous 
option. 
Yes 
Use a response type of Generate 
Application Event, clear the Synchronous 
option. 
No 
Script in form 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, with the 
SYNCHRONOUS( ) parameter. 
Yes 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, without the 
SYNCHRONOUS( ) parameter. 
No 
Middle 
Custom IDO 
method 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of True. 
Yes 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of False. 
No 
Database 
T-SQL 
Use the command: EXEC FireEventSp 
Yes 
Use the command: EXEC PostEventSp 
No 
Any 
An event action 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(true). 
Yes 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(false). 
No 
An event trigger 
Select the Synchronous option. 
Yes 
Clear the Synchronous option. 
No

Summary of synchronous functionality 
Source 
Synchronous? 
Consists of 
Requester 
Initial 
executor 
Framework 
Yes 
Synchronous (none 
marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
IDO Runtime 
IDO Runtime 
Database 
Database 

*From Appendix C: Expression Grammar (page 131):*

Framework event parameters: 
PROPERTY (Id, <Numeric Exp>, <String Exp>) 
PROPERTY (Id, <Numeric Exp>, <Typeless Exp>) 
PROPERTY (Id, <Typeless Exp>, <String Exp>) 
PROPERTY (Id, <Typeless Exp>, <Typeless Exp>) 
P (Id, <Numeric Exp>, <String Exp>) 
P (Id, <Numeric Exp>, <Typeless Exp>) 
P (Id, <Typeless Exp>, <String Exp>) 
P (Id, <Typeless Exp>, <Typeless Exp>) 
PROPERTY (<Numeric Exp>, <String Exp>) 
PROPERTY (<Numeric Exp>, <Typeless Exp>) 
PROPERTY (<Typeless Exp>, <String Exp>) 
PROPERTY (<Typeless Exp>, <Typeless Exp>) 
P (<Numeric Exp>, <String Exp>) 
P (<Numeric Exp>, <Typeless Exp>) 
P (<Typeless Exp>, <String Exp>) 
P (<Typeless Exp>, <Typeless Exp>) 
PROPERTY (<String Exp>) 
PROPERTY (<Typeless Exp>) 
P (<String Exp>) 
P (<Typeless Exp>) 
METHODPARM (<Numeric Exp>)
METHODPARM (<Typeless Exp>)
Sub-expression: 
(<Typeless Exp>) 
Parameter list 
A parameter list is a comma-separated list of scalar expressions of any type. 
<Parameter List> consists of one of these: 
<Scalar Exp> 
<Scalar Exp>, <Parameter List> 
Scalar tuples 
A scalar tuple is a parenthesized set of one or more scalar expressions. 
<Scalar Tuple> consists of this: 
(<Scalar Expr Set>)

Scalar expression sets 
A scalar expression set is a semi-colon-separated list of one or more scalar expressions, as in this. 
<Scalar Expr Set> consists of one of these: 
<Scalar Exp>; <Scalar Expr Set> 
<Scalar Exp> 
String rules
A string expression is a concatenation of expressions of type String or of unknown type (see the 
second restriction under Restrictions on page 132). 
<String Exp> consists of one of these: 
<String Value> 
<String Exp> + <String Value> 
<String Exp> + <Typeless Value> 
A string value can be any of these: 
z
A string literal 
z
A quoted variable reference 
z
A function call returning a string value 
z
A string sub-expression enclosed in parentheses 
<String Value> consists of one of these: 
StringLiteral 
<FilterIdValue> 
IF (<Boolean Exp>, <String Exp>, <String Exp>) 
IF (<Boolean Exp>, <String Exp>, <Typeless Exp>) 
IF (<Boolean Exp>, <Typeless Exp>, <String Exp>) 
String built-in functions: 
CLIENTSUBSTITUTE (<String Exp>, <String Expr List>)
CLIENTSUBSTITUTE (<Typeless Exp>, <String Expr List>)
SUBSTITUTE (<String Exp>, <String Expr List>) 
SUBSTITUTE (<Typeless Exp>, <String Expr List>) 
SUBSTRING (<String Exp>, <Numeric Exp>) 
SUBSTRING (<String Exp>, <Typeless Exp>) 
SUBSTRING (<String Exp>, <Numeric Exp>, <Numeric Exp>) 
SUBSTRING (<String Exp>, <Numeric Exp>, <Typeless Exp>) 
SUBSTRING (<String Exp>, <Typeless Exp>, <Numeric Exp>) 
SUBSTRING (<String Exp>, <Typeless Exp>, <Typeless Exp>) 
SUBSTRING (<Typeless Exp>, <Numeric Exp>)

SUBSTRING (<Typeless Exp>, <Typeless Exp>) 
SUBSTRING (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
SUBSTRING (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
SUBSTRING (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
SUBSTRING (<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
UPPER (<String Exp>) 
UPPER (<Typeless Exp>) 
LOWER (<String Exp>) 
LOWER (<Typeless Exp>) 
REPLACE (<String Exp>, <String Exp>, <String Exp>) 
REPLACE (<String Exp>, <String Exp>, <Typeless Exp>) 
REPLACE (<String Exp>, <Typeless Exp>, <String Exp>) 
REPLACE (<String Exp>, <Typeless Exp>, <Typeless Exp>) 
REPLACE (<Typeless Exp>, <String Exp>, <String Exp>) 
REPLACE (<Typeless Exp>, <String Exp>, <Typeless Exp>) 
REPLACE (<Typeless Exp>, <Typeless Exp>, <String Exp>) 
REPLACE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
Event attributes: 
EVENTNAME() 
ORIGINATOR() 
CONFIGNAME() 
EVENTSTATE() 
EVENTTITLE() 
ACTIONTYPENAME ()
VOTINGRESULT (<EventActionRef>) 

*From Appendix E: Synchronization of Metadata (page 159):*

Infor creates a framework event with three handlers 
The Infor framework team creates an event, FrameEvent, and creates three event handlers that 
execute in order when the event is generated. 
This event and these handlers are all included with the application software when it ships. 
Note that, if a "lower-level" developer wants to add or modify handlers, these rules apply: 
z
Lower-level handler creators cannot change the sequence of higher-level handlers. 
z
Any handlers lower-level creators want to use that will affect the sequence in specific ways 
must be associated with a particular, already-existing handler, using the Keep With and 
Chronology fields.

A business partner creates an additional handler 
An Infor business partner decides to add a handler that will execute just after the first framework 
handler. The business partner creates the event handler and uses the Keep With and 
Chronology fields to keep their handler with ID 1 (S1) and to execute After that handler. 
The sequence is now this:  
Note that, when the new event handler is saved, the system automatically assigns new Handler 
Sequence numbers, so that you can tell which handler executes in what order. 
The business partner uses the App Metadata Sync or App Metadata Transport utility to export the 
new metadata, along with the existing metadata, to a file that can be imported by the end-
customer. 
The business partner then sells the add-on product to the end-customer. The add-on product 
includes this file, along with any product code the business partner has developed. 
The end-customer creates three more handlers 
When the end-customer receives the add-on software from the third-party business partner, in 
addition to whatever other software installation procedures the customer must perform, the 
customer must also use the App Metadata Sync or App Metadata Transport utility to import the 
event metadata from the business partner. 
The end-customer now decides to use a different handler in place of the second framework 
handler. The customer also wants two custom handlers to run just before the third framework 
handler. To accomplish this, the customer:

z
Creates a handler and uses the Keep With field to assign this handler to ID 2 (S2). In the 
Chronology field, the customer selects Instead. 
z
Creates a second handler and uses the Keep With field to assign this handler to ID 3 (S3). In 
the Chronology field, the customer selects Before. 
z
Creates a third handler and uses the Keep With field to also assign this handler to ID 3 (S3). 
In the Chronology field, again the customer selects Before. 
After saving their new handlers with the existing handlers, the sequence is now this:  
Again, note that, when the customer saves the new handlers, the system automatically assigns 
and displays the correct Handler Sequence number on the Event Handlers form. The 
underlying Handler IDs, however, remain unchanged. 
Note that event handler S2 is now inactive and does not execute at all. It is still in the system, but 
the system ignores it in favor of the new customer handler. 
Note also that the custom handlers C2 and C3 execute in that order unless you use the Up / 
Down buttons on the Event Handler Sequence form to alter the default order.

Using non-specific chronology 
A second way for downstream developers to affect the sequence of handlers is with the use of non-
specific chronology. Non-specific chronology allows developers to indicate that a particular handler 
should always execute either first or last. 
This is done by selecting either the First or Last option from the Chronology drop-down field, as in 
this example. 
Infor creates an event with no handler 
The Infor development team adds code to generate a new application event (AppEvent) before a 
certain transaction posting is performed. 
The transaction data is passed into the event and received from the event, so that any 
downstream subscribers can test and modify the values before the posting is performed if they 
want. An event failure is trapped and aborts the posting, displaying the error message returned by 
the event. Infor adds no event handlers for the event at this time.  
The product is then released. The event is now published and available to downstream 
developers who install this product. 
An end-customer creates a handler 
An end-customer installs the software and decides to create a handler (EC1) to validate that the 
posting data is within a certain range. If it detects an out-of-range condition, the handler fails the 
event and aborts the posting.

At this point, the sequence is this:  
Because no upstream handlers exist yet (and the end-customer is the furthest downstream 
developer), a specific chronology cannot be specified at this time. 
A business partner creates an add-on product 
In the meantime, an Infor business partner creates an add-on product that stores custom 
parameters that can be used to adjust the transaction data before posting. They add their own 
handler (BP1) to input, adjust, and output the data. 
In the Chronology field, they select First to indicate that handler BP1 should run before: 
z
Any existing, downstream handlers with no specified chronology that might already exist for 
this published event 
z
Any future upstream or peer handlers 
Note: A specific chronology (Before, After, Instead) takes precedence over a non-
specific one (First and Last).

With this add-on product, at the business partner level, the sequence is now this:  
The end-customer installs the business partner’s add-on product 
Now the end-customer purchases and installs the add-on from the Infor business partner and 
uses the App Metadata Sync or App Metadata Transport utility to synchronize the metadata from 
the business partner with their own.

Because the business partner specified that their handler should always run first, the sequence is 
now this:  
The end-customer rearranges the sequence 
After installing the business partner’s add-on product, the end-customer decides that their handler 
really should run before the business partner’s. So the end-customer uses the Keep With and 
Chronology fields to associate handler EC1 with the business partner’s handler (BP1) and to 
execute Before it.

*From Appendix F: Event Flow Options (page 187):*

event handler is uniquely identified in the system with the combination of an event name and a 
handler sequence number. Each event handler is comprised of one or more event actions and, 
optionally, an initial state. 
For more information, see ”About event handlers” on page 3-36. 
event handler state 
A set of data that shows the current state of a running or finished event handler. This data includes 
information about when the event handler started running, its current status, timeout settings, and 
other information.

event initial variable 
See "initial variable." 
event input parameter 
A named static value that is passed to an event upon its triggering. This value can be set to be 
available as an output after the event finishes executing. 
Any number of uniquely named event input parameters can be collected before firing an event. Upon 
firing the event, each is converted to an event parameter. 
event message 
A message, initiated by the event system, sent from one system user to another, that in many 
respects simulates an e-mail message. Event messages are created by event actions of a Notify or 
Prompt type, or by Inbox activities such as Forward, Reply, and Reply All, or from the Send 
Message form. 
Event messages can appear in the Sent Items folder of the sender, and the Inbox of each recipient. 
For more information, see ”Event Messages” on page 5-57. 
event output parameter 
A named static value passed from an event upon its finish. Any number of uniquely named event 
output parameters can be associated with an event. Each output is created from an event parameter 
marked for output. 
event parameter 
A named storage area retrievable by an event action, that is associated with an event that has been 
generated and is processing. The system creates event parameters from event input parameters 
when the event is generated. 
Event parameters can be set to be available to whatever process generated the event, after the event 
finishes. In this case, they can also be set by event actions and can result in the creation of event 
output parameters. 
event queue 
A FIFO list of events and event handlers to be processed asynchronously. Each entry has an 
associated user name, configuration name, and request date. 
event state 
1. A collection of data related to the current status of a running or finished event. This status is viewed 
using the Event Status form. 
2. An optional text string that displays on the Event Status form when the event reaches certain 
milestones or finishes executing successfully. This text string is defined by the event handler's 
creator and associated with the Achieve Milestone and Finish action types as a parameter. 
event trigger 
A condition that causes an event to be generated with optional parameters. 
For more information, see ”About event triggers” on page 3-34.

event variable 
A named storage area, the value of which can be set and retrieved by an event action associated with 
a running event handler. When associated with a synchronous event handler, an event variable can 
be designated as Persistent, in which case the value of the variable can be passed on to the next 
event handler. 
FIFO 
First In, First Out. 
framework 
The multi-tiered software structure that makes up the entire system. In this application, the framework 
consists of three basic tiers: 
z
The client tier, known as WinStudio. 
z
The middle tier 
z
The database tier 
For more information, see the "System Architecture" chapter in your System Administration Guide. 
framework event 
An event which has been designed to be generated only in reference to certain framework 
occurrences. 
initial variable 
A named static value for an event variable associated with an event handler. This value provides the 
initial value of the event variable when the event handler begins executing. 
Each event variable contains an authorization level that provides a default access within the scope of 
an event action that: 
z
Does not have a default access value defined on the Variable Access tab of the Event Actions 
form. In this case, default access value is determined on the Event Variable Groups form. 
z
Has a default access of Default on the Variable Access tab of the Event Actions form. 
metadata 

information about data formats that are interpreted during run time, rather than compiled code (also 
called "procedural code"). 
middle tier 
The layer of software in the database system which provides the connections between the client tier 
(WinStudio) and the database tier. The middle tier has two primary functions: 
z
To provide access from the client tier to the database through IDOs (Intelligent Data Objects). The 
client tier never communicates directly with the database. In this respect, the middle tier can be 
thought of rather like a telephone: It allows two parties to talk to one another, but not face-to-face. 
z
To receive form-rendering requests from the client tier, retrieve the appropriate form-rendering 
data from the forms database, and return that data to the client so that the form displays correctly. 
For more information about the middle tier, see the "System Architecture" chapter in your System 
Administration Guide.

synchronous event handler
An event handler designed to execute sequentially with other handlers, and whose triggering process 
blocks while waiting for it to finish (unless part of an event fired asynchronously). If any one event 
handler in the sequence fails, then the whole sequence fails. 
See also "asynchronous event handler." 
transactional events or event handlers 

### Common Framework Events

| Event Name | Trigger | Description |
|-----------|---------|-------------|
| `IdoOnItemInsert` | After record insert | Fires after a new record is inserted via IDO |
| `IdoOnItemUpdate` | After record update | Fires after an existing record is updated via IDO |
| `IdoOnItemDelete` | After record delete | Fires after a record is deleted via IDO |
| `IdoOnLoadCollection` | After collection load | Fires after an IDO collection is loaded |
| `IdoOnPreItemInsert` | Before record insert | Fires before insert, can cancel operation |
| `IdoOnPreItemUpdate` | Before record update | Fires before update, can cancel operation |
| `IdoOnPreItemDelete` | Before record delete | Fires before delete, can cancel operation |

---

## Event Handler Configuration

### Handler Properties

| Property | Description |
|----------|-------------|
| Handler Name | Unique identifier for the handler |
| Description | Human-readable description of handler purpose |
| Event Name | Which event triggers this handler (e.g., `IdoOnItemUpdate`) |
| IDO Name | Which IDO this handler monitors |
| Condition | Expression that must evaluate to true for handler to execute |
| Execution Order | Numeric priority (lower = earlier execution) |
| Synchronous | Whether handler runs synchronously or asynchronously |
| Active | Whether handler is currently enabled |

*From Chapter 1: About the Application Event System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .7 (page 3):*

Workflow event handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .12

How events are handled. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
When events can be generated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
Where events can be generated  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Controlling the sequence of event handlers and actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Restricting which handlers run . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Using event handler settings  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Using the Session Access As form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Synchronicity  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Synchronous events. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Asynchronous events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Suspension. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is not suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Payload  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Adjournment and resumption . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success, failure, and retries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21

*From Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31 (page 4):*

Retrying event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23
Transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .24
Transactions with synchronous events. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .24
Event handlers marked Transactional . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .25
Event handler not marked Transactional . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .26
Rolling back transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .26
The Framework Event Service . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Setting up the Framework Event Service . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Processing order in the Framework Event Service  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Administrative details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28
Events and event handler revisions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28
Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31

About the Access As identifier . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31
About events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .32
About event triggers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .34
About event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .36
About event actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .37
About event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .38
About event action parameter forms  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .40
About event variables and initial states  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .41
About event global constants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .42

Setting up custom events and handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .45
Designing a custom event  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .46
About event handling and order . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .47
Determining names of IDO collections and components . . . . . . . . . . . . . . . . . . . . . . . . . . . .48
Refreshing the metadata cache . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .50
Chapter 4: Tracking Event System Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Handler Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Queue form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Revisions form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55
Event Handler Revisions form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55

*From Appendix D: Sample Stored Procedures. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157 (page 6):*

Maintaining handler IDs through metadata updates. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Protecting running events from metadata changes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Detailed examples  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Using specific chronology. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .162
Using non-specific chronology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .165
Performing upgrades . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .173
Overriding others’ handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .177
Non-exclusive overrides . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .178
Exclusive overrides. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .180
Disabling the ability to override. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .182
Dealing with obsolete handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .182
Appendix F: Event Flow Options . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
Glossary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
Index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 197

*From Chapter 1: About the Application Event (page 7):*

have multiple triggers and can be generated by user actions, conditions in a database, other 
events, or other situations. 
z
Event handlers consist of data that specifies: 
z
The events to which they are to respond 
z
Any conditions, situations, or attributes that determine when and why each handler executes 
z
One or more event actions to take place during the handler’s execution 
Each event can have multiple handlers but each handler can be associated with only one event. 
z
Event actions consist of instructions that specify the individual tasks or bits of work that are 
performed by the event handler. Each event handler must have at least one action and can have 
multiple actions. 

This diagram is an example of one possible set of events, event handlers, and event actions.  
For example, you might want the system to automatically notify you whenever someone adds a 
customer order to the system and to request your approval if the order is $1000 or more. In this 
example: 
z
The event in this case gets triggered whenever someone creates a new customer order. 
z
The event and the situation that tells the event handler to run are set up as part of the event 
handler definition. 
z
The event action that you want to take place is a notification that an order has been placed. You 
also want that event action to request approval for orders of $1000 or more. 
z
Only a single event handler is needed here. But that event handler requires several actions to 
complete all the requirements: 
z
The first action must check the amount of the order and determine, on the basis of the 
amount, what additional actions are required. If the order is $1000 or more, then it must direct 
the flow to another action that requests a manager’s approval. If the order is less than $1000, 
then it directs the flow to a different action that simply sends out a notification that the order 
has been placed. 
z
The second action is used only if the order is $1000 or more. If this action is used, the system 
generates a prompt message to the manager, requesting approval for the order. The system 
then waits until the manager responds. If the manager approves the order, the system then 
proceeds to the next action. If the manager does not approve the order, the event handler fails 
and no further action is taken. (Though, as good general practice, you should provide for this 
eventuality as well; but, in the interest of keeping this example simple, we will not provide for 
the case where the order is not approved.) 
z
The third action is used regardless of the amount of the order. This action sends out a 
notification to let the manager know that the order has been completed.

Conceptually, the event and associated handlers might look like this:  
For more examples, including the processes to create them, see Appendix A, "Sample Scenarios.” 

Events and event handlers are tagged at the time of their creation with a special identifier (Access As) 
that prevents them from being modified or deleted by other development organizations. Among other 
things, this prevents your custom events and handlers from being overwritten when Infor or another 
developer issues updates to their events and handlers. 

application code to generate events, and for developers and system administrators to create handlers 
for those events. Event handlers can augment or replace the default framework or application 
behavior associated with the event. You can design event handlers so that maximal work can be 
performed without requiring new procedural code. 
This is possible because event handlers are defined using metadata. Metadata, in this context, refers 
to the practice of using uncompiled code and information about data formats that are interpreted 
during run time, rather than compiled code (called here "procedural code").

See Chapter 3, “Designing and Using Events and Handlers.” 

z

performs without having to modify the basic code. Business processes are, therefore, "softer" and 
easier to modify. You can modify application processes and policies without having to directly 
modify the application code and, in many cases, without having to write any procedural code at 
all. This means that the amount of procedural code required to implement functionality can be 
greatly reduced or even eliminated altogether. 
z
You can use your event handlers with events created by others to gain control of the application 
flow and take appropriate action, rather than being forced to call into the application using APIs. 
z
Because event handlers are defined using metadata, there is no upgrade problem, and no 
collision problem if other developers also have event handlers for the same event. 

*From Chapter 2: How the Application Event (page 13):*

Events are generated (or fired) in response to an action or condition that occurs in the system. When 
the event is generated, it can execute one or more event handlers with the event actions associated 
with each event handler. 
How events are handled 
Essentially, when an event is generated, it requires an event handler to do something in response. 
Otherwise, the event serves no practical purpose. That is, if there is no handler for an event, the event 
actually does nothing when it is generated. 
TIP: That does not mean that an event should never exist unless it has an event handler. Infor 
includes some framework events as part of the system. Infor does not include handlers for these 
events. These events were created to provide events that other developers can use with their own 
custom event handlers. 
When events can be generated 
An application event can be generated when: 
z
A system user performs a particular action, perhaps only on a given form and/or when a particular 
business process is involved. 
z
A database calculation is performed, perhaps resulting in a certain value. 
z
Another event results in generating this event. 
z
A certain amount of time has passed. 
These are all examples of situations and conditions that can fire events: 
z
A sales representative saves a record in the Customers form. 
z
A manager changes the credit hold status of a customer. 
z
A factory manager adds a new item to the list of those being manufactured in that facility.

z
The first day of each month arrives. (An event can be used to generate a monthly report, for 
instance.) 
z
The quantity-on-hand of a particular item becomes less than zero. 
Where events can be generated 

z
In the client tier, the event can be generated by using a form that has a form event handler with a 
response type of Generate Application Event. 
z
In the middle tier, the event can be generated by invoking an appropriate .NET method. 
z
In the database tier, the event can be generated by using an appropriate stored procedure. 
z
In any tier, an event can generate another event by using the GenerateEvent action type. 
For details on how to generate an event from any of these locations, see “Firing events” on page 120. 
Controlling the sequence of event handlers and 
actions 
Two types of settings control the order in which event handlers and their actions execute: 
z
Each event handler has a handler sequence number. Handlers execute in the order of their 
sequence numbers. 
To modify the flow and change handler sequence order, use the Keep With and Chronology 
options on the Event Handlers form or the Event Handler Sequence form. 
See “About event handling and order” on page 47. 
z
The event actions associated with each event handler also have their own action sequence 
numbers. These execute in numeric order, unless: 
z
You use the Initial Action option on the Event Handlers form to designate that a particular 
action should execute first. 
z
You use certain event action types to modify the flow. 
See “About event actions” on page 37. 
Restricting which handlers run 
There might be times when you want or need to disable the event handlers created by one or more 
development organizations, including yours, at least temporarily. This would occur typically when you

are troubleshooting problems with the application event system. The system offers two basic ways to 
disable event handlers. 
Using event handler settings 
When you want to disable only certain event handlers temporarily, use the Active check box on the 
Event Handlers form. 
You can only disable (or enable) event handlers that have the same Access As identifier that you 
have. You cannot, for instance, use this technique to disable Core event handlers. 
Using the Session Access As form 
When you want to disable (or enable) all the event handlers created by a particular developing 
organization all at once, you can use the Session Access As form to accomplish this. 
Note: An alternate way to accomplish the same thing for individual handlers with your Access As 

*From Chapter 3: Designing and Using Events (page 31):*

and Handlers 
Infor has built in to the system a number of events and handlers that are available for immediate use. 
In addition, if you have an add-on product distributed by one of Infor’s business partners, they might 
also have added their own events and handlers that you can use. 
You can also design and create your own custom events and handlers to automate tasks for your 
particular needs. This chapter provides information about the key elements of the Application Event 
System and the procedures for creating and using custom events and handlers. 
Note: If you are creating and using your own custom events and handlers, we recommend that you 
refresh the metadata cache periodically. This should be done after doing development work, before 
testing, and after synchronizing your metadata on your system. See “Refreshing the metadata cache” 
on page 50. 

applicable, procedures for creating and using various elements are also provided. 
About the Access As identifier 

is used to: 
z
Indicate who (what organization) created and "owns" an event or related event system object. 
z
Prevent unauthorized developers from modifying or deleting event system objects that they do 
not own. 
The Access As identifier is also used to indicate ownership and modification rights for certain IDO 
metadata. It might also be used in the future for other, similar metadata. 
Generally, the Access As identifier falls into one of three classifications:

z
Core – Indicates that the object is one that Infor created and owns. These event system objects 
are used for the framework forms and operations. 
z
Any other name – Indicates that the object was created by and belongs to an application created 
either by Infor or by one of Infor’s business partners or other authorized vendors. 
z
Blank – Indicates that the object was created by and belongs to the end customer. 
Within WinStudio, several forms include an Access As field. On the Access As form, this field 
indicates the current Access As value. This is the value assigned to any new event system objects 
you might create. On all other forms, this field indicates who has ownership of the pertinent object 
metadata, in other words, who created and owns it. 
You can only modify or delete metadata for event system objects that have the same value as on the 
Access As form, in other words, application event system objects that your organization has created 
and owns. 
Note: If you need to change the Access As identifier, see the online help for the procedure. 
With a few exceptions (noted where applicable), you can attach your own event triggers and handlers 
to event system objects owned by other organizations (that is, with a different Access As identifier 
than yours), but you cannot directly modify or delete those event system objects. 
About events 
An event is defined as a uniquely named situation that can be triggered by: 
z
An action performed by somebody working in the system. 
z
A particular condition that occurs while the system is running. 
z
A certain value that is exceeded in a database record. 
z
Another event’s handler. 
z
Other, similar occurrences. 
Event types 
Events can be one of three general types: 
z
Core, or framework, events – These are events that Infor has defined and built in to the system. 
They are tagged with an Access As identifier of Core. 
These events generally fall into one of two categories: 
z
IDO (business process-related) events that are generated when certain IDOs are invoked. 
These IDOs include IdoOnItemInsert, IdoOnLoadCollection, IdoOnInvoke, and others. You 
can identify these events easily by their names, which begin with the letters Ido. 
z
Session events that are generated when certain session activities take place. 
These include SessionOnLogin, SessionOnLogout, and SessionOnVarChanged. 
These events are always synchronous and transactional. Some can be optionally suspended to 
await user responses.

z
Application-specific events – These are events that typically have been created by Infor, its 
business partners, and authorized vendors. They are tagged with an Access As identifier that 
indicates what application or development organization they belong to. 
z
Customer-defined events – These are events that a developer in an end-customer organization 
has created. They are tagged with a blank Access As identifier, which indicates that they were 
created by and belong to the customer. 

*From Chapter 4: Tracking Event System Status (page 53):*

finished executing. Some of these forms also allow you to temporarily adjust the behavior of handler 
execution. 
These forms are located in the Explorer under Master Explorer > System > Event System. 
Initially, these forms can be accessed only by members of the System Administration authorization 
group. 
These forms can all be used to track various aspects of event system status: 
z
Event Status form 
z
Event Handler Status form 
z
Event Queue form 
z
Event Revisions form 
z
Event Handler Revisions form 
z
Suspended Updates form 
Event Status form 
Use the Event Status form to view: 
z
The status of events that are currently running 
z
The history of events that have finished running 
This form has five tabs: 
z
Event tab – Provides options to filter for events and handlers in various states and make it easier 
to locate specific ones. 
For example, suppose you want to find data about all events that are currently suspended. With 
Filter-in-Place, you would select the Suspended check box and then execute Filter-in-Place. 
z
Handlers tab – Shows data about handlers that are currently processing or have finished 
processing.

z
Parameters tab – Shows data about the parameters associated with an event that is currently 
running. These include input parameters passed into the event, as well as output parameters 
created by handlers’ actions. 
z
Output Parameters tab – Shows data about the output parameters of an event that has finished 
running. 
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Handler Status form 
Use the Event Handler Status form to view: 
z
The status of event handlers that are currently running 
z
The history of event handlers that have finished running 
This form has four tabs: 
z
Handler tab – Shows data about the event handler itself. 
z
Actions tab – Shows only data about actions of the handler that have started. 
z
Variables tab – Shows information about variables associated with the event handler.
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Queue form 
The Event Queue form displays a list of all asynchronous events and event handlers that the system 
has queued for processing. All information on this form is display-only. (For more information about 
synchronous and asynchronous events and handlers, see “Synchronicity” on page 16.) 
Events on the queue are processed in FIFO (first in, first out) order. The ID number on this form 
indicates the order in which events are queued for processing. 
This form also displays other information about events and event handlers that have been queued for 
processing. Each event or event handler that has been queued is displayed as a separate record in 
the grid view. 
For more information about this form and its options, see the online help.

Event Revisions form 
The Event Revisions form displays information about the event revisions associated with events. 
For more information about event revisions and how they work, see “Events and event handler 
revisions” on page 28. 
Event Handler Revisions form 
The Event Handler Revisions form shows information about event handler revisions associated with 
event handlers. All information on this form is display-only. The reason for this is that some running or 
finished handlers are using the metadata in this revision to complete their processing. To change the 
data for this event handler, you must use the Event Handlers form. 

*From Chapter 5: Event Messages (page 57):*

The system, as part of an event handler’s actions 
Only Notify and Prompt action types can generate messages. 
z
Other users on the system, much like e-mail 
Each message is visible only by the recipients and, optionally, the sender of that message. 
Event message-related forms 
Event message-related forms are used to view, sort, file, respond to, and send messages generated 

> Messages folder. 

z
The Inbox form 
z
The Saved Messages form 
z
The Send Message form 
The Inbox form 
The Inbox form can be accessed in a number of different ways: 
z
From the View menu, by selecting the Inbox Form option. 
z
In the Windows taskbar (notifications area), by double clicking the Inbox notification icon ( 
 ). 
z
In the same ways that any other forms are accessed. 
The Inbox form displays system messages that can come from two possible sources: 
z
Application events that employ a Notify or Prompt action type. 
z
Communications initiated and sent by individual system users to other users on the system.

This form displays only those messages which are still in the recipient’s Inbox "folder" and not 
messages that have been moved to other folders. To view those messages, recipients must use the 
Saved Messages form. The Inbox form also does not allow recipients to move messages to other 
"folders." To do that, recipients must use the Saved Messages form. 
See “The Saved Messages form” on page 59. 
When a message is received, if the recipient has set options to be notified, the system alerts the 
recipient with the selected notifications. 
See the topic "Notifications Settings" in the online help. 
Recipients can mark messages as read and, depending on how and why the message was sent, 
make other responses. 
Responding to system-generated messages 
If the message is the result of a system-generated prompt, each recipient can respond to the prompt, 
usually by means of a set of voting buttons. 
See “Prompts and responses” on page 61. 
If the message was also sent to the recipient’s external e-mail inbox, and the recipient responded to 
the e-mail message, the message in the refreshed Inbox is marked as expired and the buttons are 
inactive, so the recipient cannot respond twice. 
If the message is system-generated and involves variables, for each variable, depending on the 
Variable Access setting for the event variable (on the Event Actions form) or initial state (on the 
Event Variable Groups form) or payload status (on the Event Action Notify or Event Action 
Prompt form), recipients might be able to: 
z
Provide an optional response 
z
Provide a mandatory response 
z
Only read the variable value 
z
Not see the variable value at all 
Setting variable access 
The effective visibility and writability of each variable displayed on the Inbox form is determined by 
two things: 
z
What type of action generated the message (Notify or Prompt) 
z
The (optional) variable access level as specified on the Event Action form for the action itself 
and/or on the Event Variable Groups form for the event handler’s initial state and/or on the 
Event Action Notify or Event Action Prompt form for the action with regard to the payload 
status of the property that corresponds to the variable, when the handler is associated with an 
IDO event.

For Notify type messages 
The default for variable access is Read-Only. You can use the variable access options to override this 
to Hidden for each variable. 
For Prompt type messages 
The default for variable access is Writable. You can use the variable access options to override this 
to Hidden, Read-Only, or Mandatory for each variable. 
To change the value of a variable that might appear with a message in the Inbox form, you can do 
any of these actions: 

*From Appendix A: Sample Scenarios (page 67):*

is described and then a proposed solution involving events, handlers, and/or triggers. These solutions 
are presented in a step-by-step format, as examples that you can learn from and possibly modify for 
your own use.
Note: 
z
To a certain extent, each scenario builds on the concepts and practices of previous scenarios, so 
the most effective way to use them is to work through them sequentially. However, each scenario 
is also more-or-less "self-contained" and can be used independently of the others. 
z
To see a graphical representation for each flow as you work on it, you can use the Diagram 
button on the Event Handlers form. This button opens the Event Handler Diagram form, which 
you can use to view the flow of the event handler as well as access the Event Actions form to 
edit individual actions. For more information, see the online help for the Event Handler Diagram 
form. 
This list is a list of the scenarios included in this appendix: 
Sending notifications 
z
Scenario 1: Notification of a new record—adding a user on page 68 – A simple notification is 
sent to a credit manager when a new customer is added to the database. 
z
Scenario 2: Notification of changes to an existing record—changing the credit limit on page 74 
– The credit manager is notified by e-mail that a customer’s credit limit has been changed and 
is told what the new credit limit is. 
z
Scenario 3: Notification that includes an "old" value on page 78 – A group of inventory 
stockers are automatically notified whenever an item’s lot size changes. In the message that 
is sent, both the previous lot size and the new lot size are included.
Requesting approvals 
z
Scenario 4: Approval for a new record on page 84 – A purchasing manager is prompted for 
approval whenever a new purchase order is requested.

z
Scenario 5: Requesting approval by external e-mail for changes to an existing record on page 
90 – A credit manager is prompted through an external e-mail for approval of a change to a 
customer’s credit limit. 
z
Scenario 6: Requesting multiple and complex approvals on page 97 – A purchasing manager 
is prompted for approval on a purchase order (PO) both of a change in status to Ordered and 
for the amount of the PO. If the PO is for an amount greater than $100,000, a supervisor is 
also prompted for approval. If the PO is for an amount greater than $1,000,000, two senior-
level executives must also approve it. 
Modifying records 
z
Scenario 7: Adding information to a record on page 109 – A credit manager is prompted to 
provide a credit limit for a new customer, by means of a response to a message. 
Voting
z
Scenario 8: Voting for various choices on page 111– Several managers are prompted to 
approve an engineering change, by means of a response to a message. 
Localizing message contents
z
Scenario 9: Translating captions in a purchase request on page 113 – A message containing 
localizable strings is created. 
More advanced scenarios 
z
Scenario 10: Opening a session in a remote environment on page 115 – A remote site or 
Mongoose environment is accessed to retrieve data. The details of and procedure for this 
scenario are in the Integrating IDOs with External Applications guide. 
z
Scenario 11: Cross-site event firing - adding a message to another site's Inbox on page 116 – 
A message is sent to another site’s Inbox form by using a GenericNotify event.
Sending notifications 
One of the simplest uses of the event system is to set up situations in which message notifications are 
sent out automatically to specified individuals whenever a situation occurs or a condition is met. The 
scenarios in this section illustrate this kind of situation. 
Scenario 1: Notification of a new record—adding a user 
Suppose you have a system administrator who wants to be notified whenever a new user is added to 
the system, regardless of who adds the user. Of course, you can simply require each employee who

adds users to the system to manually send a notice whenever a user is added. But that places an 
additional burden on the employee and is prone to possible oversight. 
A simple event and handler 

added. In this example, you do not need to create an event, because Infor provides an event named 
IdoPostItemInsert that you can use. All you need to do is create an event handler for that event and 
assign an action to it that generates and sends the message to the system administrator. 
We could use the IdoOnItemInsert framework event instead of the IdoPostItemInsert event. This will 
be significant when we get to the section on  Refining the message on page 71. The advantage of 
using the IdoPostItemInsert event is that, if you allow the Users form to auto-assign the user ID 

*From Appendix B: Reference Tables (page 119):*

Event handler in 
form 
Use a response type of Generate 
Application Event, select the Synchronous 
option. 
Yes 
Use a response type of Generate 
Application Event, clear the Synchronous 
option. 
No 
Script in form 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, with the 
SYNCHRONOUS( ) parameter. 
Yes 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, without the 
SYNCHRONOUS( ) parameter. 
No 
Middle 
Custom IDO 
method 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of True. 
Yes 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of False. 
No 
Database 
T-SQL 
Use the command: EXEC FireEventSp 
Yes 
Use the command: EXEC PostEventSp 
No 
Any 
An event action 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(true). 
Yes 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(false). 
No 
An event trigger 
Select the Synchronous option. 
Yes 
Clear the Synchronous option. 
No

Summary of synchronous functionality 
Source 
Synchronous? 
Consists of 
Requester 
Initial 
executor 
Framework 
Yes 
Synchronous (none 
marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
IDO Runtime 
IDO Runtime 
Database 
Database 
Synchronous (some 
marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
(validating 

*From Appendix C: Expression Grammar (page 131):*

ANYHANDLERSFAILED ( ) 
HANDLERSYNCHRONOUS ( )
HANDLERSUSPENDS ( )
HANDLERTRANSACTIONAL ( )
HANDLERIGNORESFAILURE ( )
VOTINGDISPARITY (<EventActionRef>) 
VOTINGTIE (<EventActionRef>) 
HASBEGUN (<EventActionRef>) 
HASFINISHED (<EventActionRef>) 
INSIDEDATABASE ( )

PROPERTYMODIFIED (<String Exp>)
PROPERTYMODIFIED (<Typeless Exp>)
Sub-expression: 
(<Boolean Exp>) 
Typeless rules 
A typeless expression is a concatenation or sum of elements whose type (between String, Numeric, 
and Date) we cannot distinguish without context. 
<Typeless Exp> consists of one of these: 
<Typeless Exp> + <Typeless Value> 
<Typeless Value> 
A typeless value can be any of these: 
z
A variable reference 
z
A function call whose type cannot be determined without context 
z
A typeless sub-expression enclosed in parentheses 
<Typeless Value> consists of one of these: 
<IdValue> 
IF (<Boolean Exp>, <Typeless Exp>, <Typeless Exp>) 
DBFUNCTION (<Parameter List>)

Framework event parameters: 
PROPERTY (Id, <Numeric Exp>, <String Exp>) 
PROPERTY (Id, <Numeric Exp>, <Typeless Exp>) 
PROPERTY (Id, <Typeless Exp>, <String Exp>) 
PROPERTY (Id, <Typeless Exp>, <Typeless Exp>) 
P (Id, <Numeric Exp>, <String Exp>) 
P (Id, <Numeric Exp>, <Typeless Exp>) 
P (Id, <Typeless Exp>, <String Exp>) 
P (Id, <Typeless Exp>, <Typeless Exp>) 
PROPERTY (<Numeric Exp>, <String Exp>) 
PROPERTY (<Numeric Exp>, <Typeless Exp>) 
PROPERTY (<Typeless Exp>, <String Exp>) 
PROPERTY (<Typeless Exp>, <Typeless Exp>) 
P (<Numeric Exp>, <String Exp>) 
P (<Numeric Exp>, <Typeless Exp>) 
P (<Typeless Exp>, <String Exp>) 
P (<Typeless Exp>, <Typeless Exp>) 
PROPERTY (<String Exp>) 
PROPERTY (<Typeless Exp>) 
P (<String Exp>) 
P (<Typeless Exp>) 
METHODPARM (<Numeric Exp>)
METHODPARM (<Typeless Exp>)
Sub-expression: 
(<Typeless Exp>) 
Parameter list 
A parameter list is a comma-separated list of scalar expressions of any type. 
<Parameter List> consists of one of these: 
<Scalar Exp> 
<Scalar Exp>, <Parameter List> 
Scalar tuples 
A scalar tuple is a parenthesized set of one or more scalar expressions. 
<Scalar Tuple> consists of this: 
(<Scalar Expr Set>)

Scalar expression sets 
A scalar expression set is a semi-colon-separated list of one or more scalar expressions, as in this. 
<Scalar Expr Set> consists of one of these: 
<Scalar Exp>; <Scalar Expr Set> 
<Scalar Exp> 
String rules
A string expression is a concatenation of expressions of type String or of unknown type (see the 
second restriction under Restrictions on page 132). 
<String Exp> consists of one of these: 
<String Value> 
<String Exp> + <String Value> 
<String Exp> + <Typeless Value> 

*From Appendix D: Sample Stored Procedures (page 157):*

@anyHandlersFailed [tinyint], 
@result [nvarchar](4000), 
@Infobar [nvarchar](4000) 
EXEC @Severity = FireEventSp 
@eventName = SetCoitemDueDate', 
@configName = 'SyteLine', 
@sessionID = @SessionID, 
@eventTrxId = null, 
@eventParmId = @MyEventParmID OUTPUT, 
@transactional = 0, 
@anyHandlersFailed = @anyHandlersFailed output, 
@result = @result output, 
@Infobar = @infobar output 
IF @Severity > 0 
BEGIN 
EXEC RaiseError @Infobar, @Severity 
ROLLBACK TRANSACTION 
END 
... 
COMMIT TRANSACTION

*From Appendix E: Synchronization of Metadata (page 159):*

Update any changed handlers that they own. 
z
Insert any new handlers they might have created since the last version. 
z
Maintain other owners’ handlers and the relationships between them. 
Therefore, a synchronization mechanism is needed, to make sure that changes by one metadata 
owner do not adversely affect the functioning of another owner’s metadata. 
This mechanism is provided in two components: 
z
The Access As identifier (see “About the Access As identifier” on page 31) 
z
The App Metadata Sync and App Metadata Transport utilities, which both provide the capability to 
synchronize event metadata belonging to different owners. 
Using these utilities, you can export your events and event handlers and make them available for 
import by other metadata owners. You can also use these utilities to import your own or others’ 
metadata into your system. 
For more information about these utilities, see the online help for each utility.

The inherent hierarchy of metadata 

however, an inherent hierarchy, based on the normal production flow and use of the system software. 
As illustrated in this diagram, Infor’s framework developers are the first to develop event system 
objects. Other Infor application developers then can add their own event system objects, as can 
authorized business partners and other vendor developers. Finally, end customers can make custom 
modifications and develop their own custom event system objects.  
In reality, the system is designed so that no metadata owner can modify or delete the metadata of 
another owner. So, in that sense, they are all equal. However, this real-time production flow creates 
an inherent hierarchy that allows us to think of them as "higher-level" (that is, Infor) and "lower-level" 
(that is, end-customer) owners. 
With that in mind, we can state these general rules: 
z
Lower-level owners can insert their handlers between two higher-level handlers for the same 
event. 
z
In many cases, lower-level owners can override higher-level handlers. 
There is, however, an option for higher-level owners to disallow overrides for individual handlers. 
z
Higher-level handlers that are overridden remain in the metadata store but are marked as 
Inactive. 
This means, among other things that, if the lower-level handler is later deleted, the higher-level 
handler is still available and can become active again. 
Chronology rules allow downstream owners to integrate and control the sequence of their events and 
handlers with respect to those upstream. For more information, see “Detailed examples” on 
page 161.

Maintaining handler IDs through metadata updates 
Each event handler is identified with a unique (and hidden) ID, which is referenced by the Keep With 
field on the Event Handlers form. This ID, rather than the actual Handler Sequence number, 
becomes the "fixed" reference point for that handler. This means that an event handler owner does 
not need to worry about maintaining the Handler Sequence numbers across releases: The system 
takes care of it automatically, by preserving the hidden ID number and reassigning Handler 
Sequence numbers as required. 
After each insertion, update, or deletion of a handler, and during a merge performed by the App 
Metadata Sync utility or the App Metadata Transport utility, the system calculates new integers, if 
necessary, for display in the Handler Sequence field. The underlying ID, however, remains 
unchanged. When a handler is deactivated and another added in the same position, the new handler 
gets a new ID. 
Protecting running events from metadata changes 
Once an event handler begins executing, it is essential to prevent changes to its attributes and 
actions. Otherwise, unpredictable behavior could result, especially if actions are resequenced. 
One way to prevent these changes would be to make a copy of all active, non-obsolete handlers and 
their actions each time an event is triggered and control execution from this copy. However, that 
method would result in the persistence of a great number of identical copies, assuming that handlers 
are modified much less frequently than they are executed. 
Since the system stores state data separately from metadata, it is sufficient to make a copy only when 
the metadata changes, and furthermore only when the corresponding event is triggered and a copy of 
the last metadata modifications has not yet been made. 
In other words, handler metadata for an event can be created and edited as many times as 
necessary. The first time the event is triggered, a copy of the last saved metadata is made. This copy 
is called an event revision. The execution of the event's handlers is then controlled by the event 
revision and not by the original metadata (which happen to be identical at this point). 
The event can be triggered as many times as necessary, all the time controlled by this event revision, 
as long as no intervening modifications have been made to the original metadata. 
After one or more metadata edits have been saved, though, the next time the event is triggered, the 
system copies a new event revision from the last-saved metadata. 
For more information about event revisions, see “Events and event handler revisions” on page 28. 
Detailed examples 
This section provides three detailed examples of how sequencing and synchronization work in the 

Using specific chronology 

*From Appendix F: Event Flow Options (page 187):*

encounters an adjourning event action, the event handler state is set to retest or to time out after a 
specified time. The event system then processes it at the next opportunity and resumes. 
asynchronous event handler
An event handler designed to execute independently of other event handlers, and whose triggering 
process does not block while waiting for it to finish. These event handlers are sent to an event queue, 
from which they execute in FIFO order. 
See also "asynchronous event handler." 
database tier 
That part of the system framework that stores the actual data for: 
z
Rendering forms (the Forms database) 
z
Storing all customer business data (the Application database) 
Programs can also run in this tier, where they can access data very quickly without having to traverse 
network paths. 
For more information, see the "System Architecture" chapter in your System Administration Guide. 
end-customer 
The company that has bought and is using the Infor Mongoose software. They might also have 
bought one or more add-on products by Infor business partners to customize and enhance the 
performance of their system. 
Explorer 
A window in the application (similar to Windows Explorer) that displays folders containing form 
names, providing a means to find, organize, and open forms. Explorer is the default window when the 
application opens. To reopen Explorer if it is closed, select View > Explorer on the menu bar. 
event 
A uniquely named incident that can be triggered by: 
z
An action performed by somebody working in the system 
z
A particular condition that occurs while the system is running 
z
A certain value being exceeded in a database record

z
Another event or one its handlers 
z
Other, similar occurrences 
A particular event can possibly be triggered by multiple situations or conditions, and you can 
determine how the system responds to each situation. 
To be useful, an event must have one or more event handlers defined to respond to the event. 
For more information, see ”About events” on page 3-32. 
event action 
Metadata that specifies a unit of work to perform during the execution of an event handler. A single 
event handler can have multiple event actions. Depending on its action type, an event action can do 
such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event. 
z
Set event variables. 
z
Call methods. 
z
Perform other predefined tasks. 
For more information, see ”About event actions” on page 3-37. 
event action state 
A set of data that shows the current state of a running or finished event action. This data includes 
information about when the event action started running, its current status, the number of times it has 
run, and other information. 
event action type 
A designator that limits or directs what an event action can do. This designator essentially determines 
the unit of work that each event action performs. 
event global constant 
A named static value that event expressions can reference during processing of an event handler. 
event handler 
Metadata that defines a portion of work to be performed upon the firing of a particular event. Each 
event handler is uniquely identified in the system with the combination of an event name and a 
handler sequence number. Each event handler is comprised of one or more event actions and, 
optionally, an initial state. 
For more information, see ”About event handlers” on page 3-36. 
event handler state 
A set of data that shows the current state of a running or finished event handler. This data includes 
information about when the event handler started running, its current status, timeout settings, and 
other information.

event initial variable 

---

## Action Types

Actions are the individual steps executed within an event handler. They run in sequence order and can use expressions for dynamic values.

### Action Type Reference

| Action Type | Purpose | Key Parameters |
|------------|---------|----------------|
| `SetVariable` | Assign a value to a variable | Variable name, Expression value |
| `SetPropertyValue` | Set an IDO property value | Property name, Value expression |
| `RaiseError` | Raise an error to the user | Error message expression |
| `CallMethod` | Call an IDO method | Method name, Parameters |
| `CallSubroutine` | Call another handler as subroutine | Handler name |
| `SendEmail` | Send email notification | To, Subject, Body expressions |
| `StartWorkflow` | Start an ION workflow instance | Workflow name, Input variables |
| `CallWorkflow` | Call ION workflow and wait for response | Workflow name, Variables |
| `Trigger` | Fire a custom event | Event name, Parameters |
| `ExecuteIDOSql` | Execute SQL via IDO | SQL expression |
| `ConditionalAction` | If/Then/Else logic | Condition, True actions, False actions |

*From Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31 (page 4):*

About event triggers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .34
About event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .36
About event actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .37
About event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .38
About event action parameter forms  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .40
About event variables and initial states  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .41
About event global constants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .42

Setting up custom events and handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .45
Designing a custom event  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .46
About event handling and order . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .47
Determining names of IDO collections and components . . . . . . . . . . . . . . . . . . . . . . . . . . . .48
Refreshing the metadata cache . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .50
Chapter 4: Tracking Event System Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Handler Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Queue form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Revisions form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55
Event Handler Revisions form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55

*From Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57 (page 5):*

Event action types  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Expressions and functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Pre-parser functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .127
Expression operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .128
Appendix C: Expression Grammar  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Restrictions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Start symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Character sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133

*From Chapter 1: About the Application Event (page 7):*

have multiple triggers and can be generated by user actions, conditions in a database, other 
events, or other situations. 
z
Event handlers consist of data that specifies: 
z
The events to which they are to respond 
z
Any conditions, situations, or attributes that determine when and why each handler executes 
z
One or more event actions to take place during the handler’s execution 
Each event can have multiple handlers but each handler can be associated with only one event. 
z
Event actions consist of instructions that specify the individual tasks or bits of work that are 
performed by the event handler. Each event handler must have at least one action and can have 
multiple actions. 

This diagram is an example of one possible set of events, event handlers, and event actions.  
For example, you might want the system to automatically notify you whenever someone adds a 
customer order to the system and to request your approval if the order is $1000 or more. In this 
example: 
z
The event in this case gets triggered whenever someone creates a new customer order. 
z
The event and the situation that tells the event handler to run are set up as part of the event 
handler definition. 
z
The event action that you want to take place is a notification that an order has been placed. You 
also want that event action to request approval for orders of $1000 or more. 
z
Only a single event handler is needed here. But that event handler requires several actions to 
complete all the requirements: 
z
The first action must check the amount of the order and determine, on the basis of the 
amount, what additional actions are required. If the order is $1000 or more, then it must direct 
the flow to another action that requests a manager’s approval. If the order is less than $1000, 
then it directs the flow to a different action that simply sends out a notification that the order 
has been placed. 
z
The second action is used only if the order is $1000 or more. If this action is used, the system 
generates a prompt message to the manager, requesting approval for the order. The system 
then waits until the manager responds. If the manager approves the order, the system then 
proceeds to the next action. If the manager does not approve the order, the event handler fails 
and no further action is taken. (Though, as good general practice, you should provide for this 
eventuality as well; but, in the interest of keeping this example simple, we will not provide for 
the case where the order is not approved.) 
z
The third action is used regardless of the amount of the order. This action sends out a 
notification to let the manager know that the order has been completed.

Conceptually, the event and associated handlers might look like this:  
For more examples, including the processes to create them, see Appendix A, "Sample Scenarios.” 

Events and event handlers are tagged at the time of their creation with a special identifier (Access As) 
that prevents them from being modified or deleted by other development organizations. Among other 
things, this prevents your custom events and handlers from being overwritten when Infor or another 
developer issues updates to their events and handlers. 

application code to generate events, and for developers and system administrators to create handlers 
for those events. Event handlers can augment or replace the default framework or application 
behavior associated with the event. You can design event handlers so that maximal work can be 
performed without requiring new procedural code. 
This is possible because event handlers are defined using metadata. Metadata, in this context, refers 
to the practice of using uncompiled code and information about data formats that are interpreted 
during run time, rather than compiled code (called here "procedural code").

See Chapter 3, “Designing and Using Events and Handlers.” 

z

performs without having to modify the basic code. Business processes are, therefore, "softer" and 
easier to modify. You can modify application processes and policies without having to directly 
modify the application code and, in many cases, without having to write any procedural code at 
all. This means that the amount of procedural code required to implement functionality can be 
greatly reduced or even eliminated altogether. 
z
You can use your event handlers with events created by others to gain control of the application 
flow and take appropriate action, rather than being forced to call into the application using APIs. 
z
Because event handlers are defined using metadata, there is no upgrade problem, and no 
collision problem if other developers also have event handlers for the same event. 

*From Chapter 2: How the Application Event (page 13):*

In any tier, an event can generate another event by using the GenerateEvent action type. 
For details on how to generate an event from any of these locations, see “Firing events” on page 120. 
Controlling the sequence of event handlers and 
actions 
Two types of settings control the order in which event handlers and their actions execute: 
z
Each event handler has a handler sequence number. Handlers execute in the order of their 
sequence numbers. 
To modify the flow and change handler sequence order, use the Keep With and Chronology 
options on the Event Handlers form or the Event Handler Sequence form. 
See “About event handling and order” on page 47. 
z
The event actions associated with each event handler also have their own action sequence 
numbers. These execute in numeric order, unless: 
z
You use the Initial Action option on the Event Handlers form to designate that a particular 
action should execute first. 
z
You use certain event action types to modify the flow. 
See “About event actions” on page 37. 
Restricting which handlers run 
There might be times when you want or need to disable the event handlers created by one or more 
development organizations, including yours, at least temporarily. This would occur typically when you

are troubleshooting problems with the application event system. The system offers two basic ways to 
disable event handlers. 
Using event handler settings 
When you want to disable only certain event handlers temporarily, use the Active check box on the 
Event Handlers form. 
You can only disable (or enable) event handlers that have the same Access As identifier that you 
have. You cannot, for instance, use this technique to disable Core event handlers. 
Using the Session Access As form 
When you want to disable (or enable) all the event handlers created by a particular developing 
organization all at once, you can use the Session Access As form to accomplish this. 
Note: An alternate way to accomplish the same thing for individual handlers with your Access As 
value is to open the Event Handler form and for each event handler that you do not want to include in 
testing or debugging, clear the Active check box. 
An example 
Suppose, for example, that a customer is having a problem that he suspects is being caused by 
something he did in the event system, but he is not sure what. He places a call to Infor technical 
support, and the technical support representative wants to verify that the customer’s custom event 
handlers are not causing the problem. 
In this case, the technical support representative might ask the customer to temporarily disable all 
custom event handlers so that the operation can be tested with only standard functionality in place. 
The technical support representative might instruct the customer to use the Session Access As form 
to perform either of these actions: 
z
In the Include Access As field, specify Core,BaseAppAccessAs where BaseAppAccessAs is 
the Access As identifier associated with the base application installed on the system. 
With this setting, only the Infor core (framework) and base application event handlers will execute. 
Custom event handlers created by the end-customer do not execute. 
See “Session Access As form options” on page 16. 
z
Leave the Exclude Access As field blank, and select the Exclude Blank Access As check box. 
This option allows all Infor and business partners event handlers to operate. Only the customer’s 
event handlers are ignored. 
See “Session Access As form options” on page 16.

Session Access As form options 
To disable or enable event handlers using the Session Access As form, use any of these options: 
Note: You are not obligated to use both the Include Access As and the Exclude Access As fields. 
You can use any combination of the options available on this form. 
z
With the Session Access As form open, in the Include Access As field, specify the Access As 
identifiers for event handlers that are to be recognized during this session. 
To include multiple Access As identifiers, list them separated only by commas (no spaces). 
If this field is left blank, the system can recognize and execute all event handlers. 
z
In the Exclude Access As field, specify the Access As identifiers for event handlers that are to 
be ignored during this session. 
To exclude multiple Access As identifiers, list them separated only by commas (no spaces). 
If this field is left blank, the system can recognize and execute all event handlers. The exception 
to this occurs only if the Exclude Blank Access As check box is selected. In this case, all event 
handlers are recognized except event handlers for which the Access As identifier is null (blank). 
z
To exclude those event handlers that have a blank Access As identifier, select the Exclude Blank 
Access As check box. 
Synchronicity 

of event handlers to run independently from other event handlers. Events are said to be 

*From Chapter 3: Designing and Using Events (page 31):*

With a few exceptions (noted where applicable), you can attach your own event triggers and handlers 
to event system objects owned by other organizations (that is, with a different Access As identifier 
than yours), but you cannot directly modify or delete those event system objects. 
About events 
An event is defined as a uniquely named situation that can be triggered by: 
z
An action performed by somebody working in the system. 
z
A particular condition that occurs while the system is running. 
z
A certain value that is exceeded in a database record. 
z
Another event’s handler. 
z
Other, similar occurrences. 
Event types 
Events can be one of three general types: 
z
Core, or framework, events – These are events that Infor has defined and built in to the system. 
They are tagged with an Access As identifier of Core. 
These events generally fall into one of two categories: 
z
IDO (business process-related) events that are generated when certain IDOs are invoked. 
These IDOs include IdoOnItemInsert, IdoOnLoadCollection, IdoOnInvoke, and others. You 
can identify these events easily by their names, which begin with the letters Ido. 
z
Session events that are generated when certain session activities take place. 
These include SessionOnLogin, SessionOnLogout, and SessionOnVarChanged. 
These events are always synchronous and transactional. Some can be optionally suspended to 
await user responses.

z
Application-specific events – These are events that typically have been created by Infor, its 
business partners, and authorized vendors. They are tagged with an Access As identifier that 
indicates what application or development organization they belong to. 
z
Customer-defined events – These are events that a developer in an end-customer organization 
has created. They are tagged with a blank Access As identifier, which indicates that they were 
created by and belong to the customer. 
See “About the Access As identifier” on page 31. 
Defining events 
Events can be defined (named) on these forms: 
z
Events 
z
Event Triggers 
z
Event Handlers 
To define an event, specify the name of the event in the Event Name field of one of these forms.
Note: If you do not name the event on the Events form, it is still available to the drop-down lists on 
other forms. Events named on those forms, however, do not display on the Events form. So, if you 
want the event to display on the Events form, you should name the event on that form. 
When an event is defined, or named, it is really just that: a name. Until you define a way for it to be 
triggered or initiated, the event remains just a name. This can be done using either the Event 
Triggers form, the Event Handlers form, or both. 
See “About event triggers” on page 34. 
For more information about any of these forms, see the online help for that form. 
Modifying events 
Once an event has been created and saved, the only thing you can modify is the event's description. 
The event name and other attributes are locked. 
Note: You can modify an event's description only if the Access As field has the value of the current 
Access As value, as displayed on the Access As form. 
To modify an event's description: 

Open the Events form and select the event you want to modify. 

In the Description field, modify the description text as desired. 

Save. 
Deleting events 
If you are certain you no longer need an event and you want to delete it, you can.

You can delete an event only if the Access As field has the value of the current Access As value, as 
displayed on the Access As form. 
To delete an event: 

Open the Events form and select the event you want to delete. 

From the Actions menu, select Delete. 


*From Chapter 5: Event Messages (page 57):*

Only Notify and Prompt action types can generate messages. 
z
Other users on the system, much like e-mail 
Each message is visible only by the recipients and, optionally, the sender of that message. 
Event message-related forms 
Event message-related forms are used to view, sort, file, respond to, and send messages generated 

> Messages folder. 

z
The Inbox form 
z
The Saved Messages form 
z
The Send Message form 
The Inbox form 
The Inbox form can be accessed in a number of different ways: 
z
From the View menu, by selecting the Inbox Form option. 
z
In the Windows taskbar (notifications area), by double clicking the Inbox notification icon ( 
 ). 
z
In the same ways that any other forms are accessed. 
The Inbox form displays system messages that can come from two possible sources: 
z
Application events that employ a Notify or Prompt action type. 
z
Communications initiated and sent by individual system users to other users on the system.

This form displays only those messages which are still in the recipient’s Inbox "folder" and not 
messages that have been moved to other folders. To view those messages, recipients must use the 
Saved Messages form. The Inbox form also does not allow recipients to move messages to other 
"folders." To do that, recipients must use the Saved Messages form. 
See “The Saved Messages form” on page 59. 
When a message is received, if the recipient has set options to be notified, the system alerts the 
recipient with the selected notifications. 
See the topic "Notifications Settings" in the online help. 
Recipients can mark messages as read and, depending on how and why the message was sent, 
make other responses. 
Responding to system-generated messages 
If the message is the result of a system-generated prompt, each recipient can respond to the prompt, 
usually by means of a set of voting buttons. 
See “Prompts and responses” on page 61. 
If the message was also sent to the recipient’s external e-mail inbox, and the recipient responded to 
the e-mail message, the message in the refreshed Inbox is marked as expired and the buttons are 
inactive, so the recipient cannot respond twice. 
If the message is system-generated and involves variables, for each variable, depending on the 
Variable Access setting for the event variable (on the Event Actions form) or initial state (on the 
Event Variable Groups form) or payload status (on the Event Action Notify or Event Action 
Prompt form), recipients might be able to: 
z
Provide an optional response 
z
Provide a mandatory response 
z
Only read the variable value 
z
Not see the variable value at all 
Setting variable access 
The effective visibility and writability of each variable displayed on the Inbox form is determined by 
two things: 
z
What type of action generated the message (Notify or Prompt) 
z
The (optional) variable access level as specified on the Event Action form for the action itself 
and/or on the Event Variable Groups form for the event handler’s initial state and/or on the 
Event Action Notify or Event Action Prompt form for the action with regard to the payload 
status of the property that corresponds to the variable, when the handler is associated with an 
IDO event.

For Notify type messages 
The default for variable access is Read-Only. You can use the variable access options to override this 
to Hidden for each variable. 
For Prompt type messages 
The default for variable access is Writable. You can use the variable access options to override this 
to Hidden, Read-Only, or Mandatory for each variable. 
To change the value of a variable that might appear with a message in the Inbox form, you can do 
any of these actions: 
z

*From Appendix A: Sample Scenarios (page 67):*

is described and then a proposed solution involving events, handlers, and/or triggers. These solutions 
are presented in a step-by-step format, as examples that you can learn from and possibly modify for 
your own use.
Note: 
z
To a certain extent, each scenario builds on the concepts and practices of previous scenarios, so 
the most effective way to use them is to work through them sequentially. However, each scenario 
is also more-or-less "self-contained" and can be used independently of the others. 
z
To see a graphical representation for each flow as you work on it, you can use the Diagram 
button on the Event Handlers form. This button opens the Event Handler Diagram form, which 
you can use to view the flow of the event handler as well as access the Event Actions form to 
edit individual actions. For more information, see the online help for the Event Handler Diagram 
form. 
This list is a list of the scenarios included in this appendix: 
Sending notifications 
z
Scenario 1: Notification of a new record—adding a user on page 68 – A simple notification is 
sent to a credit manager when a new customer is added to the database. 
z
Scenario 2: Notification of changes to an existing record—changing the credit limit on page 74 
– The credit manager is notified by e-mail that a customer’s credit limit has been changed and 
is told what the new credit limit is. 
z
Scenario 3: Notification that includes an "old" value on page 78 – A group of inventory 
stockers are automatically notified whenever an item’s lot size changes. In the message that 
is sent, both the previous lot size and the new lot size are included.
Requesting approvals 
z
Scenario 4: Approval for a new record on page 84 – A purchasing manager is prompted for 
approval whenever a new purchase order is requested.

z
Scenario 5: Requesting approval by external e-mail for changes to an existing record on page 
90 – A credit manager is prompted through an external e-mail for approval of a change to a 
customer’s credit limit. 
z
Scenario 6: Requesting multiple and complex approvals on page 97 – A purchasing manager 
is prompted for approval on a purchase order (PO) both of a change in status to Ordered and 
for the amount of the PO. If the PO is for an amount greater than $100,000, a supervisor is 
also prompted for approval. If the PO is for an amount greater than $1,000,000, two senior-
level executives must also approve it. 
Modifying records 
z
Scenario 7: Adding information to a record on page 109 – A credit manager is prompted to 
provide a credit limit for a new customer, by means of a response to a message. 
Voting
z
Scenario 8: Voting for various choices on page 111– Several managers are prompted to 
approve an engineering change, by means of a response to a message. 
Localizing message contents
z
Scenario 9: Translating captions in a purchase request on page 113 – A message containing 
localizable strings is created. 
More advanced scenarios 
z
Scenario 10: Opening a session in a remote environment on page 115 – A remote site or 
Mongoose environment is accessed to retrieve data. The details of and procedure for this 
scenario are in the Integrating IDOs with External Applications guide. 
z
Scenario 11: Cross-site event firing - adding a message to another site's Inbox on page 116 – 
A message is sent to another site’s Inbox form by using a GenericNotify event.
Sending notifications 
One of the simplest uses of the event system is to set up situations in which message notifications are 
sent out automatically to specified individuals whenever a situation occurs or a condition is met. The 
scenarios in this section illustrate this kind of situation. 
Scenario 1: Notification of a new record—adding a user 
Suppose you have a system administrator who wants to be notified whenever a new user is added to 
the system, regardless of who adds the user. Of course, you can simply require each employee who

adds users to the system to manually send a notice whenever a user is added. But that places an 
additional burden on the employee and is prone to possible oversight. 
A simple event and handler 

added. In this example, you do not need to create an event, because Infor provides an event named 
IdoPostItemInsert that you can use. All you need to do is create an event handler for that event and 
assign an action to it that generates and sends the message to the system administrator. 
We could use the IdoOnItemInsert framework event instead of the IdoPostItemInsert event. This will 
be significant when we get to the section on  Refining the message on page 71. The advantage of 
using the IdoPostItemInsert event is that, if you allow the Users form to auto-assign the user ID 

*From Appendix B: Reference Tables (page 119):*

Event action types 
z
Event action parameters 
z
Expressions and functions 
z
Expression operators

Firing events 
This table provides details about: 
z
Where events can be generated from (Tier) 
z
What can be used to generate them from that location (Triggered by) 
z
How to set them up (Details for construction) 
z
Whether the event is generated as a synchronous or asynchronous event (Synchronous?) 
Tier 
Triggered by 
Details for construction 
Synchronous? 
Client 
Event handler in 
form 
Use a response type of Generate 
Application Event, select the Synchronous 
option. 
Yes 
Use a response type of Generate 
Application Event, clear the Synchronous 
option. 
No 
Script in form 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, with the 
SYNCHRONOUS( ) parameter. 
Yes 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, without the 
SYNCHRONOUS( ) parameter. 
No 
Middle 
Custom IDO 
method 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of True. 
Yes 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of False. 
No 
Database 
T-SQL 
Use the command: EXEC FireEventSp 
Yes 
Use the command: EXEC PostEventSp 
No 
Any 
An event action 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(true). 
Yes 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(false). 
No 
An event trigger 
Select the Synchronous option. 
Yes 
Clear the Synchronous option. 
No

Summary of synchronous functionality 
Source 
Synchronous? 

*From Appendix C: Expression Grammar (page 131):*

For a complete list and description of KEYWORD(value) statements as they relate to action types, 
see Event action parameters on page 126
Enumerations 
These lists of keywords can be used with ACTION( ), VOTINGRULE( ), and TASKSTATUS( ) 
expressions.

ACTION( ) 
<SaveAction> consists of one of these: 
<SaveActionInsert> 
<SaveActionUpdate> 
<SaveActionDelete> 
<SaveActionInsert> consists of this: 
INSERT 
<SaveActionUpdate> consists of this: 
UPDATE 
<SaveActionDelete> consists of this: 
DELETE 
VOTINGRULE( ) 
<VotingRule> consists of one of these: 
<VotingRuleMajority> 
<VotingRulePlurality> 
<VotingRuleConditionalPlurality> 
<VotingRuleMinimumCount> 
<VotingRuleMinimumPercentage> 
<VotingRuleEarliestResponse> 
<VotingRulePreferredChoice> 
<VotingRuleMinimumCountPreferredChoice>
<VotingRuleMinimumPercentagePreferredChoice>
<VotingRuleMajority> consists of this: 
Majority 
<VotingRulePlurality> consists of this: 
Plurality 
<VotingRuleConditionalPlurality> consists of this: 
ConditionalPlurality 
<VotingRuleMinimumCount> consists of this: 
MinimumCount 
<VotingRuleMinimumPercentage> consists of this: 
MinimumPercentage

<VotingRuleEarliestResponse> consists of this: 
EarliestResponse 
<VotingRulePreferredChoice> consists of this: 
PreferredChoice 
<VotingRuleMinimumCountPreferredChoice> consists of this: 
MinimumCountPreferredChoice
<VotingRuleMinimumPercentagePreferredChoice> consists of this: 
MinimumPercentagePreferredChoice
TASKSTATUS( ) 
<InitialTaskStatus> consists of one of these: 
<TaskStatusReady> 
<TaskStatusWaiting> 
<TaskStatusReady> consists of this: 
READY 
<TaskStatusWaiting> consists of this: 
WAITING

*From Appendix D: Sample Stored Procedures (page 157):*

EXEC RaiseError @Infobar, @Severity 
ROLLBACK TRANSACTION 
END 
... 
COMMIT TRANSACTION

*From Appendix E: Synchronization of Metadata (page 159):*

their actions each time an event is triggered and control execution from this copy. However, that 
method would result in the persistence of a great number of identical copies, assuming that handlers 
are modified much less frequently than they are executed. 
Since the system stores state data separately from metadata, it is sufficient to make a copy only when 
the metadata changes, and furthermore only when the corresponding event is triggered and a copy of 
the last metadata modifications has not yet been made. 
In other words, handler metadata for an event can be created and edited as many times as 
necessary. The first time the event is triggered, a copy of the last saved metadata is made. This copy 
is called an event revision. The execution of the event's handlers is then controlled by the event 
revision and not by the original metadata (which happen to be identical at this point). 
The event can be triggered as many times as necessary, all the time controlled by this event revision, 
as long as no intervening modifications have been made to the original metadata. 
After one or more metadata edits have been saved, though, the next time the event is triggered, the 
system copies a new event revision from the last-saved metadata. 
For more information about event revisions, see “Events and event handler revisions” on page 28. 
Detailed examples 
This section provides three detailed examples of how sequencing and synchronization work in the 

Using specific chronology 
The primary way for a lower-level handler creator to resequence existing handlers (from higher-level 
owners) is to use what is known as specific chronology. That is, the handler’s creator can attach the 
new handler to an existing handler and specify the order in which the two handlers are to execute with 
respect to each other. 
The mechanism used to do this are the Keep With and Chronology fields on the Event Handlers 
form. These fields allow you to specify whether your handler should run before, after, or in place of the 
handler it is associated with, as in this example. 
For more information about the Keep With and Chronology fields, see the online help for those 
fields. 
Infor creates a framework event with three handlers 
The Infor framework team creates an event, FrameEvent, and creates three event handlers that 
execute in order when the event is generated. 
This event and these handlers are all included with the application software when it ships. 
Note that, if a "lower-level" developer wants to add or modify handlers, these rules apply: 
z
Lower-level handler creators cannot change the sequence of higher-level handlers. 
z
Any handlers lower-level creators want to use that will affect the sequence in specific ways 
must be associated with a particular, already-existing handler, using the Keep With and 
Chronology fields.

A business partner creates an additional handler 
An Infor business partner decides to add a handler that will execute just after the first framework 
handler. The business partner creates the event handler and uses the Keep With and 
Chronology fields to keep their handler with ID 1 (S1) and to execute After that handler. 
The sequence is now this:  
Note that, when the new event handler is saved, the system automatically assigns new Handler 
Sequence numbers, so that you can tell which handler executes in what order. 
The business partner uses the App Metadata Sync or App Metadata Transport utility to export the 
new metadata, along with the existing metadata, to a file that can be imported by the end-
customer. 
The business partner then sells the add-on product to the end-customer. The add-on product 
includes this file, along with any product code the business partner has developed. 
The end-customer creates three more handlers 
When the end-customer receives the add-on software from the third-party business partner, in 
addition to whatever other software installation procedures the customer must perform, the 
customer must also use the App Metadata Sync or App Metadata Transport utility to import the 
event metadata from the business partner. 
The end-customer now decides to use a different handler in place of the second framework 
handler. The customer also wants two custom handlers to run just before the third framework 
handler. To accomplish this, the customer:

z
Creates a handler and uses the Keep With field to assign this handler to ID 2 (S2). In the 
Chronology field, the customer selects Instead. 
z
Creates a second handler and uses the Keep With field to assign this handler to ID 3 (S3). In 
the Chronology field, the customer selects Before. 
z
Creates a third handler and uses the Keep With field to also assign this handler to ID 3 (S3). 
In the Chronology field, again the customer selects Before. 
After saving their new handlers with the existing handlers, the sequence is now this:  
Again, note that, when the customer saves the new handlers, the system automatically assigns 
and displays the correct Handler Sequence number on the Event Handlers form. The 
underlying Handler IDs, however, remain unchanged. 
Note that event handler S2 is now inactive and does not execute at all. It is still in the system, but 
the system ignores it in favor of the new customer handler. 
Note also that the custom handlers C2 and C3 execute in that order unless you use the Up / 
Down buttons on the Event Handler Sequence form to alter the default order.

Using non-specific chronology 

*From Appendix F: Event Flow Options (page 187):*

An event handler designed to execute independently of other event handlers, and whose triggering 
process does not block while waiting for it to finish. These event handlers are sent to an event queue, 
from which they execute in FIFO order. 
See also "asynchronous event handler." 
database tier 
That part of the system framework that stores the actual data for: 
z
Rendering forms (the Forms database) 
z
Storing all customer business data (the Application database) 
Programs can also run in this tier, where they can access data very quickly without having to traverse 
network paths. 
For more information, see the "System Architecture" chapter in your System Administration Guide. 
end-customer 
The company that has bought and is using the Infor Mongoose software. They might also have 
bought one or more add-on products by Infor business partners to customize and enhance the 
performance of their system. 
Explorer 
A window in the application (similar to Windows Explorer) that displays folders containing form 
names, providing a means to find, organize, and open forms. Explorer is the default window when the 
application opens. To reopen Explorer if it is closed, select View > Explorer on the menu bar. 
event 
A uniquely named incident that can be triggered by: 
z
An action performed by somebody working in the system 
z
A particular condition that occurs while the system is running 
z
A certain value being exceeded in a database record

z
Another event or one its handlers 
z
Other, similar occurrences 
A particular event can possibly be triggered by multiple situations or conditions, and you can 
determine how the system responds to each situation. 
To be useful, an event must have one or more event handlers defined to respond to the event. 
For more information, see ”About events” on page 3-32. 
event action 
Metadata that specifies a unit of work to perform during the execution of an event handler. A single 
event handler can have multiple event actions. Depending on its action type, an event action can do 
such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event. 
z
Set event variables. 
z
Call methods. 
z
Perform other predefined tasks. 
For more information, see ”About event actions” on page 3-37. 
event action state 
A set of data that shows the current state of a running or finished event action. This data includes 
information about when the event action started running, its current status, the number of times it has 
run, and other information. 
event action type 
A designator that limits or directs what an event action can do. This designator essentially determines 
the unit of work that each event action performs. 
event global constant 
A named static value that event expressions can reference during processing of an event handler. 
event handler 
Metadata that defines a portion of work to be performed upon the firing of a particular event. Each 
event handler is uniquely identified in the system with the combination of an event name and a 
handler sequence number. Each event handler is comprised of one or more event actions and, 
optionally, an initial state. 
For more information, see ”About event handlers” on page 3-36. 
event handler state 
A set of data that shows the current state of a running or finished event handler. This data includes 
information about when the event handler started running, its current status, timeout settings, and 
other information.

event initial variable 
See "initial variable." 
event input parameter 
A named static value that is passed to an event upon its triggering. This value can be set to be 

---

## Expression Syntax

AES uses a custom expression language for conditions, variable assignments, and action parameters.

### Expression Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `EXPR()` | `EXPR(expression)` | Evaluate an expression |
| `GETVALUE()` | `GETVALUE(property)` | Get current value of an IDO property |
| `GETOLDVALUE()` | `GETOLDVALUE(property)` | Get previous value (before update) |
| `ISNULL()` | `ISNULL(value, default)` | Return default if value is null |
| `CONVERT()` | `CONVERT(value, type)` | Type conversion |
| `CurrentUser` | `CurrentUser()` | Returns current user identity |
| `CurrentDate` | `CurrentDate()` | Returns current date |
| `CurrentDateTime` | `CurrentDateTime()` | Returns current date/time |

### Operators

| Operator | Description |
|----------|-------------|
| `=`, `<>` | Equal, Not equal |
| `<`, `>`, `<=`, `>=` | Comparison |
| `AND`, `OR`, `NOT` | Logical |
| `+`, `-`, `*`, `/` | Arithmetic |
| `LIKE` | Pattern matching |
| `IN` | Set membership |

*From Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57 (page 5):*

Appendix A: Sample Scenarios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
Sending notifications  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .68
Requesting approvals. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .84
Modifying records . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .109
Voting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .111
Localizing message contents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .113
More advanced scenarios  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .115
Appendix B: Reference Tables. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
Firing events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .120
Summary of synchronous functionality. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .121
Framework events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .122
Application events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .125
Event action types  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Expressions and functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Pre-parser functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .127
Expression operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .128
Appendix C: Expression Grammar  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Restrictions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Start symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Character sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133

*From Chapter 3: Designing and Using Events (page 31):*

A Boolean expression 
z
Two non-Boolean expressions separated by a comparison operator 
Examples 
z
This example causes the event to fire when seven days have elapsed since the current result of 
the database function dbo.LastEntryDate(): 
DATEDIFF(day, DBFUNCTION("LastEntryDate"), CURDATETIME()) > 7 
z
This example causes the event to fire when the balance on a certain customer's order is greater 
than $10,000: 
DBFUNCTION("OrderBalance", GC(BigCustNum)) > 10000 
z
This example causes the event to fire on the first day of each month: 
DATEPART(day, CURDATETIME()) = 1 
Note: The condition should generally involve a time operation, a database calculation, or both. This is 
because time and the database are the only known factors that can undergo change from external 
stimuli (that is, by the forward movement of time or by the actions of other application users, 
respectively). 
Retesting triggers 
When the event trigger's Retest At Date setting becomes older than the current system clock time, 
the event trigger is available to be processed by the event service. This happens when the event 
service is free from processing any waiting queued events and handlers and any already-waiting 
triggers that need to be tested or retested. 
To process the event trigger, the system parses the condition, evaluates it, and, if the condition 
evaluates to TRUE, then the event fires. At that point, the Retest At Date setting is set to the current 
time plus the amount of time set for the Trigger Reset Interval. If the Trigger Reset Interval is set to 
0 (zero), then the Active inidicator is cleared, which indicates that the trigger is not to be retested. 
If the condition evaluates to FALSE, then the Retest At Date setting is set to the current time plus the 
amount of time set for the Condition Retest Interval. If the Condition Retest Interval is set to 0 
(zero), then the Active indicator is cleared, which indicates that the trigger is not to be retested.

About event handlers 
An event handler defines the actions to be taken upon the firing of a particular event. Each event 
handler is comprised of one or more event actions and, optionally, an initial state. 
Each event can have multiple event handlers that execute when the event fires. In such cases, the 
handler sequence number and other factors determine the order in which event handlers are actually 
processed. 
For more information about event actions, see “About event actions” on page 37. 
For more information about initial states, see “About event variables and initial states” on page 41. 
Defining event handlers 
Each event handler is uniquely defined in the system by the combination of an event name and a 
handler sequence number. Both of these are set on the Event Handlers form. Event handlers also 
must have one or more associated event actions. 
See “About event actions” on page 37. 
To create an event handler: 

Open the Event Handlers form. 

Press F3. 

From the Actions menu, select New. 

In the Event Name field: 
z
Select the event for which you want to create a handler. 
This sets up the event handler for an already-defined event. 
z
Specify the name for an event which has not been previously defined. 
This effectively defines a new event as well. 

(Optional) To control the order in which the event handler executes (especially with respect to 
existing event handlers), use the Keep With and Chronology fields, or the Event Handler 
Sequence form. 
See “About event handling and order” on page 47. 

Save the new event handler. 

Use the Event Actions button to open the Event Actions form and create the actions to be 
performed when this event handler is executed. 
See “About event actions” on page 37. 

After closing the Event Actions form, set the other options on the Event Handlers form as 
desired. 
An event handler can be restricted to execute only in relation to a specific set of conditions. For 
example, a particular event handler might be defined to execute only when the associated event 
is triggered by an action on a particular form or when a particular IDO is involved.

An event handler can also be set to execute synchronously or asynchronously, or as part of a 
transactional event or set of event handlers. 
See “Synchronicity” on page 16 or “Transactions” on page 24. 
For information about the other options, see the online help for each option. 

Save the event handler. 
About event actions 
An event action is defined as a unit of work to be performed during the execution of an event handler. 
A single event handler can have multiple event actions, but each action is assigned to a single event 
handler. 
Depending on its action type, an event action can do such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event handler. 
z
Set event variables. 
z
Call methods or web services. 

*From Appendix A: Sample Scenarios (page 67):*

Appendix A: Sample Scenarios
This appendix presents a number of typical scenarios in which you might want to use the Application 
Event System to automate various tasks in response to various situations. In each case, the situation 
is described and then a proposed solution involving events, handlers, and/or triggers. These solutions 
are presented in a step-by-step format, as examples that you can learn from and possibly modify for 
your own use.
Note: 
z
To a certain extent, each scenario builds on the concepts and practices of previous scenarios, so 
the most effective way to use them is to work through them sequentially. However, each scenario 
is also more-or-less "self-contained" and can be used independently of the others. 
z
To see a graphical representation for each flow as you work on it, you can use the Diagram 
button on the Event Handlers form. This button opens the Event Handler Diagram form, which 
you can use to view the flow of the event handler as well as access the Event Actions form to 
edit individual actions. For more information, see the online help for the Event Handler Diagram 
form. 
This list is a list of the scenarios included in this appendix: 
Sending notifications 
z
Scenario 1: Notification of a new record—adding a user on page 68 – A simple notification is 
sent to a credit manager when a new customer is added to the database. 
z
Scenario 2: Notification of changes to an existing record—changing the credit limit on page 74 
– The credit manager is notified by e-mail that a customer’s credit limit has been changed and 
is told what the new credit limit is. 
z
Scenario 3: Notification that includes an "old" value on page 78 – A group of inventory 
stockers are automatically notified whenever an item’s lot size changes. In the message that 
is sent, both the previous lot size and the new lot size are included.
Requesting approvals 
z
Scenario 4: Approval for a new record on page 84 – A purchasing manager is prompted for 
approval whenever a new purchase order is requested.

z
Scenario 5: Requesting approval by external e-mail for changes to an existing record on page 
90 – A credit manager is prompted through an external e-mail for approval of a change to a 
customer’s credit limit. 
z
Scenario 6: Requesting multiple and complex approvals on page 97 – A purchasing manager 
is prompted for approval on a purchase order (PO) both of a change in status to Ordered and 
for the amount of the PO. If the PO is for an amount greater than $100,000, a supervisor is 
also prompted for approval. If the PO is for an amount greater than $1,000,000, two senior-
level executives must also approve it. 
Modifying records 
z
Scenario 7: Adding information to a record on page 109 – A credit manager is prompted to 
provide a credit limit for a new customer, by means of a response to a message. 
Voting
z
Scenario 8: Voting for various choices on page 111– Several managers are prompted to 
approve an engineering change, by means of a response to a message. 
Localizing message contents
z
Scenario 9: Translating captions in a purchase request on page 113 – A message containing 
localizable strings is created. 
More advanced scenarios 
z
Scenario 10: Opening a session in a remote environment on page 115 – A remote site or 
Mongoose environment is accessed to retrieve data. The details of and procedure for this 
scenario are in the Integrating IDOs with External Applications guide. 
z
Scenario 11: Cross-site event firing - adding a message to another site's Inbox on page 116 – 
A message is sent to another site’s Inbox form by using a GenericNotify event.
Sending notifications 
One of the simplest uses of the event system is to set up situations in which message notifications are 
sent out automatically to specified individuals whenever a situation occurs or a condition is met. The 
scenarios in this section illustrate this kind of situation. 
Scenario 1: Notification of a new record—adding a user 
Suppose you have a system administrator who wants to be notified whenever a new user is added to 
the system, regardless of who adds the user. Of course, you can simply require each employee who

adds users to the system to manually send a notice whenever a user is added. But that places an 
additional burden on the employee and is prone to possible oversight. 
A simple event and handler 

added. In this example, you do not need to create an event, because Infor provides an event named 
IdoPostItemInsert that you can use. All you need to do is create an event handler for that event and 
assign an action to it that generates and sends the message to the system administrator. 
We could use the IdoOnItemInsert framework event instead of the IdoPostItemInsert event. This will 
be significant when we get to the section on  Refining the message on page 71. The advantage of 
using the IdoPostItemInsert event is that, if you allow the Users form to auto-assign the user ID 
number (instead of specifying the user ID number yourself), the system waits until the ID number has 
been assigned before filling in the "CustNum" data in the message. If we use the IdoOnItemInsert 
event, the system does not wait, which means that, if you auto-assign the customer ID number, the 
restulting message has "TBD" in place of the actual customer number. 
To set this up: 
1.
Create the event handler: 
a.
Open the Event Handlers form. 
b.
Press F3. 
c.
Press Ctrl+N. 
d.
Create the handler with these settings:  
Field or Option 
Setting / Comments 

*From Appendix B: Reference Tables (page 119):*

Appendix B: Reference Tables
This appendix provides several reference tables containing detailed information about various 

z
Firing events 
z
Summary of synchronous functionality 
z
Framework events 
z
Application events 
z
Event action types 
z
Event action parameters 
z
Expressions and functions 
z
Expression operators

Firing events 
This table provides details about: 
z
Where events can be generated from (Tier) 
z
What can be used to generate them from that location (Triggered by) 
z
How to set them up (Details for construction) 
z
Whether the event is generated as a synchronous or asynchronous event (Synchronous?) 
Tier 
Triggered by 
Details for construction 
Synchronous? 
Client 
Event handler in 
form 
Use a response type of Generate 
Application Event, select the Synchronous 
option. 
Yes 
Use a response type of Generate 
Application Event, clear the Synchronous 
option. 
No 
Script in form 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, with the 
SYNCHRONOUS( ) parameter. 
Yes 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, without the 
SYNCHRONOUS( ) parameter. 
No 
Middle 
Custom IDO 
method 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of True. 
Yes 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of False. 
No 
Database 
T-SQL 
Use the command: EXEC FireEventSp 
Yes 
Use the command: EXEC PostEventSp 
No 
Any 
An event action 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(true). 
Yes 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(false). 
No 
An event trigger 
Select the Synchronous option. 
Yes 
Clear the Synchronous option. 
No

Summary of synchronous functionality 
Source 
Synchronous? 
Consists of 
Requester 
Initial 
executor 
Framework 
Yes 
Synchronous (none 
marked Suspend) & 

*From Appendix C: Expression Grammar (page 131):*

Appendix C: Expression Grammar 
This appendix contains the complete grammar available for constructing expressions for event action 
parameters. Major sections include: 
z
Restrictions 
z
Start symbol 
z
Character sets 
z
Terminals 
z
Rules 
z
Variable, constant, and event parameter references 
z
Expressions 
z
Boolean rules 
z
Typeless rules 
z
String rules 
z
Numeric rules 
z
Date rules 
z
Restricted arguments 
z
Keyword paren lists 
z
Enumerations

Restrictions 
Expressions in this grammar are subject to these restrictions: 
z
Superfluous parentheses are usually not allowed. 
For example, this produces a parsing error: 
V(this)=1 and 2=V(that)) and 1=(2) 
Instead, you can write it like this, to work around the grammar limitation: 
V(this)=1 and 2=V(that) and 1=2 
z
Operation chains containing a mix of typed and typeless arguments must begin with a typed 
value. 
For example, this example produces an error because the first argument is not a typed value: 
'12'=V(a)+'B'+V(c) 
Instead, and because string concatenation is not commutative, you can write it as: 
'12'=''+V(a)+'B'+V(c) 
Alternatively, you can declare the type for the first argument as: 
'12'=CAST(V(a) AS STRING)+'B'+V(c) 
Again, this example produces an error because the first argument is not a typed value: 
12>V(b)+1+5 
Instead, you can write the expression in one of these ways: 
12>0+V(b)+1+5 
12>CAST(V(b) AS NUMBER)+1+5 
12>1+V(b)+5 
The last solution works because numeric addition is commutative. 
z
Functions cannot be used for variable, parameter, or constant names. 
For example, because the letter y is an abbreviation for year in the DATEPART( ) and 
DATEDIFF( ) event functions, this expression produces an error: 
y = 5 
Instead, you can declare y as yVar. This expression does not produce an error. 
yVar = 5 
Start symbol 
"Start Symbol" = <functionParenList>

Character sets 
This table lists and describes the acceptable characters for elements of the code described. You can 
include any amount of white space between elements. 
{ID Head} = {Letter} + [_] 
{ID Tail} = {Alphanumeric} + [_] + ['['] + [']'] + [.] 
{String Ch 1} = {Printable} - ["] + {LF} + {CR} 
{String Ch 2} = {Printable} - ['] + {LF} + {CR} 
Terminals 
String constants are constructed using one of these rules. The string can be: 
z
Enclosed in double-quotes, containing no double-quote characters as illustrated by this example: 
StringLiteral = "{String Ch 1}*" 
z
Enclosed in double-quotes, containing paired double-quotes that are each interpreted as a single 
embedded double-quote character as illustrated by this example: 
StringLiteral = "(""|{String Ch 1})*" 
This 
Designates 
Number 
The set of numerals: 0123456789 
Letter 
The set of all uppercase and lowercase letters: 
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ 
Alphanumeric 
The set of all characters listed as part of the Number and 
Letter sets 
Printable 
The set of all standard characters that can be printed 
onscreen. This includes the characters from  #32 to #127 and  
#160 (nonbreaking space). The nonbreaking space character 
is included because it is often used in source code. 

*From Appendix F: Event Flow Options (page 187):*

Appendix F: Event Flow Options
The flow diagram in this appendix illustrates many of the possible ways an event can be generated 
and the types of flows that can result. This diagram highlights the differences between functionality 

Glossary 
Access As 
An identifier used to identify who created and owns a metadata object. This identifier is also used to 
control which metadata objects you can modify. You can modify only those metadata objects that are 
associated with the current Access As field value, as displayed on the Access As form.
For more information, see ”About the Access As identifier” on page 3-31. 
adjourning event 
An event action that must wait for an external stimulus before it can continue. When the system 
encounters an adjourning event action, the event handler state is set to retest or to time out after a 
specified time. The event system then processes it at the next opportunity and resumes. 
asynchronous event handler
An event handler designed to execute independently of other event handlers, and whose triggering 
process does not block while waiting for it to finish. These event handlers are sent to an event queue, 
from which they execute in FIFO order. 
See also "asynchronous event handler." 
database tier 
That part of the system framework that stores the actual data for: 
z
Rendering forms (the Forms database) 
z
Storing all customer business data (the Application database) 
Programs can also run in this tier, where they can access data very quickly without having to traverse 
network paths. 
For more information, see the "System Architecture" chapter in your System Administration Guide. 
end-customer 
The company that has bought and is using the Infor Mongoose software. They might also have 
bought one or more add-on products by Infor business partners to customize and enhance the 
performance of their system. 
Explorer 
A window in the application (similar to Windows Explorer) that displays folders containing form 
names, providing a means to find, organize, and open forms. Explorer is the default window when the 
application opens. To reopen Explorer if it is closed, select View > Explorer on the menu bar. 
event 
A uniquely named incident that can be triggered by: 
z
An action performed by somebody working in the system 
z
A particular condition that occurs while the system is running 
z
A certain value being exceeded in a database record

z
Another event or one its handlers 
z
Other, similar occurrences 
A particular event can possibly be triggered by multiple situations or conditions, and you can 
determine how the system responds to each situation. 
To be useful, an event must have one or more event handlers defined to respond to the event. 
For more information, see ”About events” on page 3-32. 
event action 
Metadata that specifies a unit of work to perform during the execution of an event handler. A single 
event handler can have multiple event actions. Depending on its action type, an event action can do 
such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event. 
z
Set event variables. 
z
Call methods. 
z
Perform other predefined tasks. 
For more information, see ”About event actions” on page 3-37. 
event action state 
A set of data that shows the current state of a running or finished event action. This data includes 
information about when the event action started running, its current status, the number of times it has 
run, and other information. 
event action type 
A designator that limits or directs what an event action can do. This designator essentially determines 
the unit of work that each event action performs. 
event global constant 
A named static value that event expressions can reference during processing of an event handler. 
event handler 
Metadata that defines a portion of work to be performed upon the firing of a particular event. Each 
event handler is uniquely identified in the system with the combination of an event name and a 
handler sequence number. Each event handler is comprised of one or more event actions and, 
optionally, an initial state. 
For more information, see ”About event handlers” on page 3-36. 
event handler state 
A set of data that shows the current state of a running or finished event handler. This data includes 
information about when the event handler started running, its current status, timeout settings, and 
other information.

event initial variable 
See "initial variable." 
event input parameter 
A named static value that is passed to an event upon its triggering. This value can be set to be 
available as an output after the event finishes executing. 
Any number of uniquely named event input parameters can be collected before firing an event. Upon 
firing the event, each is converted to an event parameter. 
event message 
A message, initiated by the event system, sent from one system user to another, that in many 

---

## Suspension & InWorkflow Pattern

When an AES handler calls an ION workflow (via `CallWorkflow`), execution can be suspended while waiting for the workflow to complete. The `InWorkflow` flag on a record indicates it is currently being processed by an ION workflow.

### Key Patterns

1. **Pre-check**: Before calling workflow, set `InWorkflow = 1` to flag the record
2. **CallWorkflow**: Start the ION workflow, passing input variables
3. **Suspension**: Handler execution pauses until workflow completes
4. **Resume**: When workflow returns, handler continues with output variables
5. **Post-action**: Process workflow results, clear `InWorkflow` flag

*From Chapter 1: About the Application Event System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .7 (page 3):*

Workflow event handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .12

How events are handled. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
When events can be generated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
Where events can be generated  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Controlling the sequence of event handlers and actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Restricting which handlers run . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Using event handler settings  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Using the Session Access As form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Synchronicity  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Synchronous events. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Asynchronous events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Suspension. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is not suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Payload  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Adjournment and resumption . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success, failure, and retries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21

*From Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57 (page 5):*

Suspended Updates form. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55
Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
Event message-related forms. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
The Inbox form. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
The Saved Messages form. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .59
The Send Message form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .60
Sending e-mail to external e-mail Inbox for prompts  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .60
Prompts and responses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .61
Voting rules. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .62
Dealing with indeterminate voting results. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .65
Quorums. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .66
Appendix A: Sample Scenarios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
Sending notifications  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .68
Requesting approvals. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .84
Modifying records . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .109
Voting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .111
Localizing message contents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .113
More advanced scenarios  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .115
Appendix B: Reference Tables. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
Firing events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .120
Summary of synchronous functionality. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .121
Framework events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .122
Application events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .125
Event action types  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Expressions and functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Pre-parser functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .127
Expression operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .128
Appendix C: Expression Grammar  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Restrictions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Start symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Character sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133

*From Chapter 2: How the Application Event (page 13):*

Unless the event is designed to suspend, the expectation is that the event will complete 
synchronously. Therefore, its synchronous event handlers execute in sequence in the same thread 
that generated it and block that thread until they have all been executed or until a handler exits with a 
failure status. 
Events are synchronous when they are generated by:

z
Core (framework) events 
z
Calling the FireApplicationEvent() .NET method with the Synchronous parameter set to True 
z
Calling the dbo.FireEventSp stored procedure 
z
Using a form event handler with a response type of Generate Application Event and the 
Synchronous option selected 
z
Using an event action of the type Generate Event and a parameter of Synchronous(True) 
Asynchronous events 
This means that the event runs in a different thread than the one that posted it, usually on a utility 
server. In this case, the event does not block the generating thread, running independently of it. As 
soon as an acknowledgment is received that the event was successfully queued, the thread that 
generated the event continues on. 
See “The Framework Event Service” on page 27. 
Events are asynchronous when they are generated by: 
z
Calling the FireApplicationEvent() .NET method with the Synchronous parameter set to False 
z
Calling the dbo.PostEventSp stored procedure 
z
Using a form event handler with a response type of Generate Application Event and the 
Synchronous option cleared 
z
Using an event action of the type Generate Event and a parameter of Synchronous with a value 
of False 
Event handlers 
Event handlers can be designated as synchronous or asynchronous at the time they are created, 
using the Synchronous check box on the Event Handlers form. 
Any event, either synchronous or asynchronous, can execute an asynchronous event handler when 
execution reaches an event handler designated as an asynchronous event handler; that is, for which 
the Synchronous check box is cleared. At this point: 
z
The system sends the asynchronous event handler to the event handler queue. 
Called queueing, the system does this by means of the PostEventHandlerSp stored procedure, to 
which it passes the configuration name from the event state. 
z
If queueing was successful, the event's thread continues on to the next event handler or, if no 
subsequent handlers are defined, completes the event. 
z
If queueing was unsuccessful, the event stops with a failure condition. 
See “Summary of synchronous functionality” on page 121.

Suspension 
Suspension occurs when a requested operation is sent to the event system for completion at a later 
time. This occurs when the event handler has the Suspend option selected and contains an 
adjourning action. 
Suspension is possible only with certain framework events. You cannot create custom events that can 
be suspended. Currently, these are the events that can be suspended: 
z
IdoOnItemInsert 
z
IdoOnItemUpdate 
z
IdoOnItemDelete 
Suspension occurs when the system generates an event that: 
z
Is one of these framework events that can be suspended. 
z
Has the Suspend check box selected (on the form) for at least one handler that applies to the 
generated event’s object and initiator. 
When an event is suspended 
When both of the above conditions are met, WinStudio passes control of the requested update 
(insertion/update/deletion) to the application event system. The application event system then tries to 
make sure the event handlers can all execute successfully before actually committing the system 
(and the data) to execution of the event actions. 
This is done in two stages. 
Suspend-validating stage 
When an event is suspended, in what is known as suspend-validating stage, the system: 

Begins a database transaction. 


*From Chapter 3: Designing and Using Events (page 31):*

These events are always synchronous and transactional. Some can be optionally suspended to 
await user responses.

z
Application-specific events – These are events that typically have been created by Infor, its 
business partners, and authorized vendors. They are tagged with an Access As identifier that 
indicates what application or development organization they belong to. 
z
Customer-defined events – These are events that a developer in an end-customer organization 
has created. They are tagged with a blank Access As identifier, which indicates that they were 
created by and belong to the customer. 
See “About the Access As identifier” on page 31. 
Defining events 
Events can be defined (named) on these forms: 
z
Events 
z
Event Triggers 
z
Event Handlers 
To define an event, specify the name of the event in the Event Name field of one of these forms.
Note: If you do not name the event on the Events form, it is still available to the drop-down lists on 
other forms. Events named on those forms, however, do not display on the Events form. So, if you 
want the event to display on the Events form, you should name the event on that form. 
When an event is defined, or named, it is really just that: a name. Until you define a way for it to be 
triggered or initiated, the event remains just a name. This can be done using either the Event 
Triggers form, the Event Handlers form, or both. 
See “About event triggers” on page 34. 
For more information about any of these forms, see the online help for that form. 
Modifying events 
Once an event has been created and saved, the only thing you can modify is the event's description. 
The event name and other attributes are locked. 
Note: You can modify an event's description only if the Access As field has the value of the current 
Access As value, as displayed on the Access As form. 
To modify an event's description: 

Open the Events form and select the event you want to modify. 

In the Description field, modify the description text as desired. 

Save. 
Deleting events 
If you are certain you no longer need an event and you want to delete it, you can.

You can delete an event only if the Access As field has the value of the current Access As value, as 
displayed on the Access As form. 
To delete an event: 

Open the Events form and select the event you want to delete. 

From the Actions menu, select Delete. 

Save. 
About event triggers 
An event trigger is defined as a condition that causes a particular event to fire, more-or-less 
independent of anything that might be happening in the user interface. The event trigger carries a set 
of event trigger parameters for use when the event fires. 
An event trigger can be set to fire the event only once, or it can be set to retest for its condition after 
waiting a certain amount of time since either of these situations was true: 
z
The trigger last successfully fired the event. 
z
The trigger last tested unsuccessfully for its condition. 
In both cases, you can set the interval for the event trigger to wait, both for the successful firing of the 
trigger and for the unsuccessful test for the trigger conditions (using separate settings). Testing and 
retesting is accomplished by means of polling; this is not a true interruptive trigger. 
An event trigger carries with it the user name and configuration in effect at the time it was defined. 
This data is passed on to the event state when the trigger fires the event. 
Defining event triggers 
Event triggers are defined using the Event Triggers form. Use this form to determine the condition 
that will fire the event, set the parameters to be passed to the event when it fires, and specify retest 
intervals. 
To create an event trigger: 

Open the Event Triggers form. 

Press F3. 

From the Actions menu, select New. 


*From Chapter 4: Tracking Event System Status (page 53):*

Suspended Updates form 
Event Status form 
Use the Event Status form to view: 
z
The status of events that are currently running 
z
The history of events that have finished running 
This form has five tabs: 
z
Event tab – Provides options to filter for events and handlers in various states and make it easier 
to locate specific ones. 
For example, suppose you want to find data about all events that are currently suspended. With 
Filter-in-Place, you would select the Suspended check box and then execute Filter-in-Place. 
z
Handlers tab – Shows data about handlers that are currently processing or have finished 
processing.

z
Parameters tab – Shows data about the parameters associated with an event that is currently 
running. These include input parameters passed into the event, as well as output parameters 
created by handlers’ actions. 
z
Output Parameters tab – Shows data about the output parameters of an event that has finished 
running. 
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Handler Status form 
Use the Event Handler Status form to view: 
z
The status of event handlers that are currently running 
z
The history of event handlers that have finished running 
This form has four tabs: 
z
Handler tab – Shows data about the event handler itself. 
z
Actions tab – Shows only data about actions of the handler that have started. 
z
Variables tab – Shows information about variables associated with the event handler.
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Queue form 
The Event Queue form displays a list of all asynchronous events and event handlers that the system 
has queued for processing. All information on this form is display-only. (For more information about 
synchronous and asynchronous events and handlers, see “Synchronicity” on page 16.) 
Events on the queue are processed in FIFO (first in, first out) order. The ID number on this form 
indicates the order in which events are queued for processing. 
This form also displays other information about events and event handlers that have been queued for 
processing. Each event or event handler that has been queued is displayed as a separate record in 
the grid view. 
For more information about this form and its options, see the online help.

Event Revisions form 
The Event Revisions form displays information about the event revisions associated with events. 
For more information about event revisions and how they work, see “Events and event handler 
revisions” on page 28. 
Event Handler Revisions form 
The Event Handler Revisions form shows information about event handler revisions associated with 
event handlers. All information on this form is display-only. The reason for this is that some running or 
finished handlers are using the metadata in this revision to complete their processing. To change the 
data for this event handler, you must use the Event Handlers form. 
For more information about event handler revisions and how they work, see “Events and event 
handler revisions” on page 28. 
Suspended Updates form 
The Suspended Updates form displays a list of all the update actions that are currently in a 
suspended state. This form also allows you to take selected updates out of suspension manually. 
For more information about this form, see the online help for the form.

*From Appendix A: Sample Scenarios (page 67):*

Suspend 
Cleared.

For more information about any of these fields and options, see the help for the Event 
Handlers form. 
e.
Save. 
2.
Define the action for the event handler you just created: 
a.
In the Event Handlers form, select the handler you created in Step 1. 
b.
Click Event Actions. 
c.
In the Event Actions form, in the Action Sequence field, specify 10. 
d.
From the Action Type drop-down list, select Notify. 
e.
Click Edit Parameters. 
f.
In the Event Action Notify form, click the To button. 
g.
In the Event Action Parameter Recipients form, from the list of recipients, select the user ID 
of the credit manager (or whoever is serving in that role).  
h.
Click Update and then OK. 
i.
In the Subject field, specify New Customer! 
j.
In the Category field, specify Change Notification.
k.
In the Body field, specify We have a new customer! 
Synchronous 
Cleared. 
Because this notification does not require any 
response from the credit manager, it can run 
asynchronously. For more information, see 
“Synchronicity” on page 16. 
Active 
Selected. 
Can Override 
Selected. 
Transactional 
Cleared. 
Obsolete 
Cleared. 
Initial State 
Leave blank. 
Initial Action 
Leave blank. 
Note: Technically, you can specify any integer you want in this field, and the 
system treats them sequential order. We recommend using multiples of ten, 
initially at least, just in case you later need to add more action steps between 
existing steps, so you do not need to renumber all existing steps. 
TIP: You can select more than one recipient. Also, to deselect a recipient, click 
the user ID again. 
Field or Option 
Setting / Comments

l.
Select the Save in Sent Items check box. 
This parameter tells the system to save a copy of the notification in the Sent Items folder of 
the person who added the new customer. 
m. Click OK. 
On the Event Actions form, in the editable field on the Parameters tab, you should see this: 
CATEGORY("Change Notification")
TO("userID") 
SUBJECT("New Customer!") 
BODY("We have a new customer!") 
SAVEMESSAGE(TRUE) 
where userID is the sign-in user ID for the credit manager.  
3.
(Optional, but recommended) To verify that there are no syntax errors, click Check Syntax. 
4.
Save the action and close the Event Actions form. 
5.
Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Test the event by using the Customers form to create a new customer. Then, sign in as the user ID 
specified in the TO parameter, open the Inbox form, and verify that the message was received. The 

*From Appendix B: Reference Tables (page 119):*

marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
IDO Runtime 
IDO Runtime 
Database 
Database 
Synchronous (some 
marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
(validating 
mode) 
Event Service 
(Committing 
mode)
IDO Runtime 
FireEvent 
OR 
Generate 
Event 
with 
Synchronous
(True) 
Yes 
Synchronous and 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
IDO Runtime 
IDO Runtime 
Database 
Database 
Event service 
Event service 
PostEvent 
OR 
Generate 
Event 
with 
Synchronous
(False) 
No 
Synchronous and 
asynchronous event 
handlers 
WinStudio 
Event service 
IDO Runtime 
Database 
Event service 
Context 
Synchronous? 
Suspending?
Event’s or 
prior event 
handler’s 
executor
Initial 
executor 
Can 
adjourn? 
Suspending 
event (always 
generated 
synchronously) 
Yes 
No 
IDO Runtime 
(validating mode) 
IDO Runtime 
No 
Event service 
(committing 
mode) 

*From Appendix C: Expression Grammar (page 131):*

HANDLERSUSPENDS ( )
HANDLERTRANSACTIONAL ( )
HANDLERIGNORESFAILURE ( )
VOTINGDISPARITY (<EventActionRef>) 
VOTINGTIE (<EventActionRef>) 
HASBEGUN (<EventActionRef>) 
HASFINISHED (<EventActionRef>) 
INSIDEDATABASE ( )

PROPERTYMODIFIED (<String Exp>)
PROPERTYMODIFIED (<Typeless Exp>)
Sub-expression: 
(<Boolean Exp>) 
Typeless rules 
A typeless expression is a concatenation or sum of elements whose type (between String, Numeric, 
and Date) we cannot distinguish without context. 
<Typeless Exp> consists of one of these: 
<Typeless Exp> + <Typeless Value> 
<Typeless Value> 
A typeless value can be any of these: 
z
A variable reference 
z
A function call whose type cannot be determined without context 
z
A typeless sub-expression enclosed in parentheses 
<Typeless Value> consists of one of these: 
<IdValue> 
IF (<Boolean Exp>, <Typeless Exp>, <Typeless Exp>) 
DBFUNCTION (<Parameter List>)

Framework event parameters: 
PROPERTY (Id, <Numeric Exp>, <String Exp>) 
PROPERTY (Id, <Numeric Exp>, <Typeless Exp>) 
PROPERTY (Id, <Typeless Exp>, <String Exp>) 
PROPERTY (Id, <Typeless Exp>, <Typeless Exp>) 
P (Id, <Numeric Exp>, <String Exp>) 
P (Id, <Numeric Exp>, <Typeless Exp>) 
P (Id, <Typeless Exp>, <String Exp>) 
P (Id, <Typeless Exp>, <Typeless Exp>) 
PROPERTY (<Numeric Exp>, <String Exp>) 
PROPERTY (<Numeric Exp>, <Typeless Exp>) 
PROPERTY (<Typeless Exp>, <String Exp>) 
PROPERTY (<Typeless Exp>, <Typeless Exp>) 
P (<Numeric Exp>, <String Exp>) 
P (<Numeric Exp>, <Typeless Exp>) 
P (<Typeless Exp>, <String Exp>) 
P (<Typeless Exp>, <Typeless Exp>) 
PROPERTY (<String Exp>) 
PROPERTY (<Typeless Exp>) 
P (<String Exp>) 
P (<Typeless Exp>) 
METHODPARM (<Numeric Exp>)
METHODPARM (<Typeless Exp>)
Sub-expression: 
(<Typeless Exp>) 
Parameter list 
A parameter list is a comma-separated list of scalar expressions of any type. 
<Parameter List> consists of one of these: 
<Scalar Exp> 
<Scalar Exp>, <Parameter List> 
Scalar tuples 
A scalar tuple is a parenthesized set of one or more scalar expressions. 
<Scalar Tuple> consists of this: 
(<Scalar Expr Set>)

Scalar expression sets 
A scalar expression set is a semi-colon-separated list of one or more scalar expressions, as in this. 
<Scalar Expr Set> consists of one of these: 
<Scalar Exp>; <Scalar Expr Set> 
<Scalar Exp> 
String rules
A string expression is a concatenation of expressions of type String or of unknown type (see the 
second restriction under Restrictions on page 132). 
<String Exp> consists of one of these: 
<String Value> 
<String Exp> + <String Value> 
<String Exp> + <Typeless Value> 
A string value can be any of these: 
z

*From Appendix F: Event Flow Options (page 187):*

suspending 2-18
synchronicity (summary) B-121
synchronous and asynchronous 2-16
transactional 2-25
Event Handlers form 3-36
event messages 5-57– 5-66
indeterminate voting results 5-65
prompts and responses 5-61
related forms 5-57
voting rules 5-62
event queue
Framework Event Service 2-27
processing order 2-27
Event Queue form 4-54
Event Revisions form 4-55
Event Status form 4-53
event triggers 3-34
defininig 3-34
retesting 3-35
setting conditions for 3-35
Event Triggers form 3-34
Event Variable Groups form 3-41
event variables 3-41
events 3-32
action types B-126
actions 3-37
asynchronous 2-17

defining 3-33
firing from tiers B-120
flow diagram 2-13
framework (core) B-122
global constants 3-42
handlers 3-36
handling 2-13
message-related forms 5-57
Inbox 5-57
Saved Messages 5-59
Send Message 5-60
naming 3-33
parameter forms 3-40
parameters 3-38
passing 3-40
setting values and variables 3-40
revisions 2-28
setting up custom 3-45
suspend-committing mode 2-19
suspending 2-18
suspend-validating mode 2-18
synchronicity (summary) B-121
synchronous 2-16
transactional 2-24
triggers 3-34
defining 3-34
examples 2-13
retesting 3-35
setting conditions for 3-35
types 3-32
variables 3-41
where they can be generated from 2-14
Events form 3-32
Exclude Blank Access As setting
(Session Access As form) 2-15
expansions for functions
complex B-127
nested B-128
simple B-127
expressions
functions
pre-parser B-127
standard B-126
grammar C-131– C-156
character sets C-133
enumerations C-154
rules C-134
start symbol C-132
terminals C-133
keyword paren lists C-154
numeric-castable C-135
operators B-128

---

## Scenario Walkthroughs

### Chapter 1: About the Application Event System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .7 (page 3)

Example 1: Sending a notification when a record is added . . . . . . . . . . . . . . . . . . . . . . . . . .10
Example 2: Getting approval for a credit limit change . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .10
Example 3: Complex approval of a purchase order status change . . . . . . . . . . . . . . . . . . . .11
Example 4: Automatically shipping a customer order. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11
Workflow event handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .12

How events are handled. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
When events can be generated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
Where events can be generated  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Controlling the sequence of event handlers and actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Restricting which handlers run . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Using event handler settings  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Using the Session Access As form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Synchronicity  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Synchronous events. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Asynchronous events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Suspension. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is not suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Payload  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Adjournment and resumption . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success, failure, and retries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21

### Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57 (page 5)

Appendix A: Sample Scenarios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
Sending notifications  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .68
Requesting approvals. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .84
Modifying records . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .109
Voting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .111
Localizing message contents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .113
More advanced scenarios  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .115
Appendix B: Reference Tables. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
Firing events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .120
Summary of synchronous functionality. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .121
Framework events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .122
Application events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .125
Event action types  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Expressions and functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Pre-parser functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .127
Expression operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .128
Appendix C: Expression Grammar  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Restrictions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Start symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Character sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133

### Appendix D: Sample Stored Procedures. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157 (page 6)

Detailed examples  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Using specific chronology. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .162
Using non-specific chronology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .165
Performing upgrades . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .173
Overriding others’ handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .177
Non-exclusive overrides . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .178
Exclusive overrides. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .180
Disabling the ability to override. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .182
Dealing with obsolete handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .182
Appendix F: Event Flow Options . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
Glossary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
Index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 197

### Chapter 1: About the Application Event (page 7)

This diagram is an example of one possible set of events, event handlers, and event actions.  
For example, you might want the system to automatically notify you whenever someone adds a 
customer order to the system and to request your approval if the order is $1000 or more. In this 
example: 
z
The event in this case gets triggered whenever someone creates a new customer order. 
z
The event and the situation that tells the event handler to run are set up as part of the event 
handler definition. 
z
The event action that you want to take place is a notification that an order has been placed. You 
also want that event action to request approval for orders of $1000 or more. 
z
Only a single event handler is needed here. But that event handler requires several actions to 
complete all the requirements: 
z
The first action must check the amount of the order and determine, on the basis of the 
amount, what additional actions are required. If the order is $1000 or more, then it must direct 
the flow to another action that requests a manager’s approval. If the order is less than $1000, 
then it directs the flow to a different action that simply sends out a notification that the order 
has been placed. 
z
The second action is used only if the order is $1000 or more. If this action is used, the system 
generates a prompt message to the manager, requesting approval for the order. The system 
then waits until the manager responds. If the manager approves the order, the system then 
proceeds to the next action. If the manager does not approve the order, the event handler fails 
and no further action is taken. (Though, as good general practice, you should provide for this 
eventuality as well; but, in the interest of keeping this example simple, we will not provide for 
the case where the order is not approved.) 
z
The third action is used regardless of the amount of the order. This action sends out a 
notification to let the manager know that the order has been completed.

Conceptually, the event and associated handlers might look like this:  
For more examples, including the processes to create them, see Appendix A, "Sample Scenarios.” 

Events and event handlers are tagged at the time of their creation with a special identifier (Access As) 
that prevents them from being modified or deleted by other development organizations. Among other 
things, this prevents your custom events and handlers from being overwritten when Infor or another 
developer issues updates to their events and handlers. 

application code to generate events, and for developers and system administrators to create handlers 
for those events. Event handlers can augment or replace the default framework or application 
behavior associated with the event. You can design event handlers so that maximal work can be 
performed without requiring new procedural code. 
This is possible because event handlers are defined using metadata. Metadata, in this context, refers 
to the practice of using uncompiled code and information about data formats that are interpreted 
during run time, rather than compiled code (called here "procedural code").

See Chapter 3, “Designing and Using Events and Handlers.” 

z

performs without having to modify the basic code. Business processes are, therefore, "softer" and 
easier to modify. You can modify application processes and policies without having to directly 
modify the application code and, in many cases, without having to write any procedural code at 
all. This means that the amount of procedural code required to implement functionality can be 
greatly reduced or even eliminated altogether. 
z
You can use your event handlers with events created by others to gain control of the application 
flow and take appropriate action, rather than being forced to call into the application using APIs. 
z
Because event handlers are defined using metadata, there is no upgrade problem, and no 
collision problem if other developers also have event handlers for the same event. 
Examples of ways to use the Application Event 
System 
These examples offer illustrations of how to use the application event system, including explanations 
of how this can benefit you. For more sample scenarios, including the procedures required to 
implement them, see Appendix A, "Sample Scenarios.” 
Example 1: Sending a notification when a record is added 
Suppose you have a sales manager who wants to be notified whenever someone adds a new 
customer to the system. You could rely on personnel compliance by anyone who has the ability to add 
customers to the system and trust them to remember to send the sales manager an e-mail. This, 
however, might not be the most reliable solution. 

can set up an event that is generated whenever anyone adds a new customer into the system, and 
use event handlers and actions to automatically generate a notification that is sent to the sales 
manager. 
For a more detailed example, including the procedure to create and use the required handlers, see 
"Sending notifications" on page 68. 
Example 2: Getting approval for a credit limit change 
Suppose your company requires that any change to a customer’s credit limit be approved by a 
designated credit manager. You could require any customer representative to contact that credit 
manager whenever a change to a credit limit is requested.

manager a message requesting approval of the change. To speed up the process, you can also send 
an e-mail to the credit manager that contains links the manager can click to approve or deny the 
request. 
When the credit manager responds to the message and approves the request, the system can then 
automatically change the credit limit amount. 
For a more detailed example, including the procedure to create and use the required handlers, see 
"Requesting approvals" on page 84. 
Example 3: Complex approval of a purchase order status change 
Suppose your company has a business process in place that: 
z
Requests approval from a purchasing manager when the status of any purchase order (PO) is 
changed to Ordered. 
z
If the purchasing manager approves the request and the total cost of the PO exceeds a certain 
amount, requests majority approval from a group of higher level managers on whether the order 
should be sent to the vendor. 
z
If those managers also approve and the total cost of the PO exceeds another, higher amount, 
requests unanimous approval from a group of top-level directors. 
z
If the request is approved at all the required levels for the total cost of the PO, the transaction is 
approved and completed. 
As with the previous two examples, this process could all be taken care of manually, involving actions 
by many employees. However, the potential amount of time consumed and the risk of something 
getting missed somewhere increases with each approval required. 
So, you could use events and handlers to automate this entire process, evaluating the PO at each 
step of the way, requesting only the necessary approvals, and completing the transaction upon 
approval. 
Example 4: Automatically shipping a customer order 
Suppose you have a system that, by default, requires someone to manually set the system to ship a 
customer order line when the the status of the line is set to Filled. This can cause delays in orders, if/
when the responsible employee does not set the order to ship in a timely manner. 

to ship as soon as the status is set to Filled.


### Chapter 2: How the Application Event (page 13)

These are all examples of situations and conditions that can fire events: 
z
A sales representative saves a record in the Customers form. 
z
A manager changes the credit hold status of a customer. 
z
A factory manager adds a new item to the list of those being manufactured in that facility.

z
The first day of each month arrives. (An event can be used to generate a monthly report, for 
instance.) 
z
The quantity-on-hand of a particular item becomes less than zero. 
Where events can be generated 

z
In the client tier, the event can be generated by using a form that has a form event handler with a 
response type of Generate Application Event. 
z
In the middle tier, the event can be generated by invoking an appropriate .NET method. 
z
In the database tier, the event can be generated by using an appropriate stored procedure. 
z
In any tier, an event can generate another event by using the GenerateEvent action type. 
For details on how to generate an event from any of these locations, see “Firing events” on page 120. 
Controlling the sequence of event handlers and 
actions 
Two types of settings control the order in which event handlers and their actions execute: 
z
Each event handler has a handler sequence number. Handlers execute in the order of their 
sequence numbers. 
To modify the flow and change handler sequence order, use the Keep With and Chronology 
options on the Event Handlers form or the Event Handler Sequence form. 
See “About event handling and order” on page 47. 
z
The event actions associated with each event handler also have their own action sequence 
numbers. These execute in numeric order, unless: 
z
You use the Initial Action option on the Event Handlers form to designate that a particular 
action should execute first. 
z
You use certain event action types to modify the flow. 
See “About event actions” on page 37. 
Restricting which handlers run 
There might be times when you want or need to disable the event handlers created by one or more 
development organizations, including yours, at least temporarily. This would occur typically when you

are troubleshooting problems with the application event system. The system offers two basic ways to 
disable event handlers. 
Using event handler settings 
When you want to disable only certain event handlers temporarily, use the Active check box on the 
Event Handlers form. 
You can only disable (or enable) event handlers that have the same Access As identifier that you 
have. You cannot, for instance, use this technique to disable Core event handlers. 
Using the Session Access As form 
When you want to disable (or enable) all the event handlers created by a particular developing 
organization all at once, you can use the Session Access As form to accomplish this. 
Note: An alternate way to accomplish the same thing for individual handlers with your Access As 
value is to open the Event Handler form and for each event handler that you do not want to include in 
testing or debugging, clear the Active check box. 
An example 
Suppose, for example, that a customer is having a problem that he suspects is being caused by 
something he did in the event system, but he is not sure what. He places a call to Infor technical 
support, and the technical support representative wants to verify that the customer’s custom event 
handlers are not causing the problem. 
In this case, the technical support representative might ask the customer to temporarily disable all 
custom event handlers so that the operation can be tested with only standard functionality in place. 
The technical support representative might instruct the customer to use the Session Access As form 
to perform either of these actions: 
z
In the Include Access As field, specify Core,BaseAppAccessAs where BaseAppAccessAs is 
the Access As identifier associated with the base application installed on the system. 
With this setting, only the Infor core (framework) and base application event handlers will execute. 
Custom event handlers created by the end-customer do not execute. 
See “Session Access As form options” on page 16. 
z
Leave the Exclude Access As field blank, and select the Exclude Blank Access As check box. 
This option allows all Infor and business partners event handlers to operate. Only the customer’s 
event handlers are ignored. 
See “Session Access As form options” on page 16.

Session Access As form options 
To disable or enable event handlers using the Session Access As form, use any of these options: 
Note: You are not obligated to use both the Include Access As and the Exclude Access As fields. 
You can use any combination of the options available on this form. 
z
With the Session Access As form open, in the Include Access As field, specify the Access As 
identifiers for event handlers that are to be recognized during this session. 
To include multiple Access As identifiers, list them separated only by commas (no spaces). 
If this field is left blank, the system can recognize and execute all event handlers. 
z
In the Exclude Access As field, specify the Access As identifiers for event handlers that are to 
be ignored during this session. 
To exclude multiple Access As identifiers, list them separated only by commas (no spaces). 
If this field is left blank, the system can recognize and execute all event handlers. The exception 
to this occurs only if the Exclude Blank Access As check box is selected. In this case, all event 
handlers are recognized except event handlers for which the Access As identifier is null (blank). 
z
To exclude those event handlers that have a blank Access As identifier, select the Exclude Blank 
Access As check box. 
Synchronicity 

of event handlers to run independently from other event handlers. Events are said to be 
“synchronous” when they must execute their handlers in a specific order. Events are said to be 
“asynchronous” when they can execute their handlers independently of other handlers. 
A synchronous event handler is one that must complete before the system continues to the next 
event handler in a sequence. For the entire event to be handled successfully, all synchronous 
handlers in the sequence must complete successfully. The exception to this rule is that, if one event 
handler fails, other than for an illegal operation, and the system is set to ignore failures for that 
handler, the system can continue to the next synchronous event handler. Otherwise, the system 
returns a failure error, and no more event handlers in the sequence execute. 
By contrast, an asynchronous event handler runs independently of other event handlers. 
Synchronous events 
Unless the event is designed to suspend, the expectation is that the event will complete 
synchronously. Therefore, its synchronous event handlers execute in sequence in the same thread 
that generated it and block that thread until they have all been executed or until a handler exits with a 
failure status. 
Events are synchronous when they are generated by:

z

### Chapter 3: Designing and Using Events (page 31)

Examples 
z
This example causes the event to fire when seven days have elapsed since the current result of 
the database function dbo.LastEntryDate(): 
DATEDIFF(day, DBFUNCTION("LastEntryDate"), CURDATETIME()) > 7 
z
This example causes the event to fire when the balance on a certain customer's order is greater 
than $10,000: 
DBFUNCTION("OrderBalance", GC(BigCustNum)) > 10000 
z
This example causes the event to fire on the first day of each month: 
DATEPART(day, CURDATETIME()) = 1 
Note: The condition should generally involve a time operation, a database calculation, or both. This is 
because time and the database are the only known factors that can undergo change from external 
stimuli (that is, by the forward movement of time or by the actions of other application users, 
respectively). 
Retesting triggers 
When the event trigger's Retest At Date setting becomes older than the current system clock time, 
the event trigger is available to be processed by the event service. This happens when the event 
service is free from processing any waiting queued events and handlers and any already-waiting 
triggers that need to be tested or retested. 
To process the event trigger, the system parses the condition, evaluates it, and, if the condition 
evaluates to TRUE, then the event fires. At that point, the Retest At Date setting is set to the current 
time plus the amount of time set for the Trigger Reset Interval. If the Trigger Reset Interval is set to 
0 (zero), then the Active inidicator is cleared, which indicates that the trigger is not to be retested. 
If the condition evaluates to FALSE, then the Retest At Date setting is set to the current time plus the 
amount of time set for the Condition Retest Interval. If the Condition Retest Interval is set to 0 
(zero), then the Active indicator is cleared, which indicates that the trigger is not to be retested.

About event handlers 
An event handler defines the actions to be taken upon the firing of a particular event. Each event 
handler is comprised of one or more event actions and, optionally, an initial state. 
Each event can have multiple event handlers that execute when the event fires. In such cases, the 
handler sequence number and other factors determine the order in which event handlers are actually 
processed. 
For more information about event actions, see “About event actions” on page 37. 
For more information about initial states, see “About event variables and initial states” on page 41. 
Defining event handlers 
Each event handler is uniquely defined in the system by the combination of an event name and a 
handler sequence number. Both of these are set on the Event Handlers form. Event handlers also 
must have one or more associated event actions. 
See “About event actions” on page 37. 
To create an event handler: 

Open the Event Handlers form. 

Press F3. 

From the Actions menu, select New. 

In the Event Name field: 
z
Select the event for which you want to create a handler. 
This sets up the event handler for an already-defined event. 
z
Specify the name for an event which has not been previously defined. 
This effectively defines a new event as well. 

(Optional) To control the order in which the event handler executes (especially with respect to 
existing event handlers), use the Keep With and Chronology fields, or the Event Handler 
Sequence form. 
See “About event handling and order” on page 47. 

Save the new event handler. 

Use the Event Actions button to open the Event Actions form and create the actions to be 
performed when this event handler is executed. 
See “About event actions” on page 37. 

After closing the Event Actions form, set the other options on the Event Handlers form as 
desired. 
An event handler can be restricted to execute only in relation to a specific set of conditions. For 
example, a particular event handler might be defined to execute only when the associated event 
is triggered by an action on a particular form or when a particular IDO is involved.

An event handler can also be set to execute synchronously or asynchronously, or as part of a 
transactional event or set of event handlers. 
See “Synchronicity” on page 16 or “Transactions” on page 24. 
For information about the other options, see the online help for each option. 

Save the event handler. 
About event actions 
An event action is defined as a unit of work to be performed during the execution of an event handler. 
A single event handler can have multiple event actions, but each action is assigned to a single event 
handler. 
Depending on its action type, an event action can do such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event handler. 
z
Set event variables. 
z
Call methods or web services. 
z
Perform other predefined tasks. 
Defining event actions 
To define new event actions, open the Event Actions form using the Event Actions button on the 
Event Handlers form. If you open the Event Actions form from the Explorer or the Select Form 
dialog box, you can only view and modify existing actions. 
To create an event action: 

Open the Event Handlers form. 

Create a new event handler; or, in the grid view, select the event handler for which you want to 
create the action. 

Click the Event Actions button. 

(If there are no existing event actions) From the Actions menu, select New. 

In the Action Sequence field, specify a number. 
This number determines the order in which actions for a particular handler are processed. 

In the Event Actions form, Action Type field, specify the type of action to be performed. 
Note: If you are creating a new handler, you must save it before you can do the next 
step.

### Chapter 4: Tracking Event System Status (page 53)

For example, suppose you want to find data about all events that are currently suspended. With 
Filter-in-Place, you would select the Suspended check box and then execute Filter-in-Place. 
z
Handlers tab – Shows data about handlers that are currently processing or have finished 
processing.

z
Parameters tab – Shows data about the parameters associated with an event that is currently 
running. These include input parameters passed into the event, as well as output parameters 
created by handlers’ actions. 
z
Output Parameters tab – Shows data about the output parameters of an event that has finished 
running. 
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Handler Status form 
Use the Event Handler Status form to view: 
z
The status of event handlers that are currently running 
z
The history of event handlers that have finished running 
This form has four tabs: 
z
Handler tab – Shows data about the event handler itself. 
z
Actions tab – Shows only data about actions of the handler that have started. 
z
Variables tab – Shows information about variables associated with the event handler.
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Queue form 
The Event Queue form displays a list of all asynchronous events and event handlers that the system 
has queued for processing. All information on this form is display-only. (For more information about 
synchronous and asynchronous events and handlers, see “Synchronicity” on page 16.) 
Events on the queue are processed in FIFO (first in, first out) order. The ID number on this form 
indicates the order in which events are queued for processing. 
This form also displays other information about events and event handlers that have been queued for 
processing. Each event or event handler that has been queued is displayed as a separate record in 
the grid view. 
For more information about this form and its options, see the online help.

Event Revisions form 
The Event Revisions form displays information about the event revisions associated with events. 
For more information about event revisions and how they work, see “Events and event handler 
revisions” on page 28. 
Event Handler Revisions form 
The Event Handler Revisions form shows information about event handler revisions associated with 
event handlers. All information on this form is display-only. The reason for this is that some running or 
finished handlers are using the metadata in this revision to complete their processing. To change the 
data for this event handler, you must use the Event Handlers form. 
For more information about event handler revisions and how they work, see “Events and event 
handler revisions” on page 28. 
Suspended Updates form 
The Suspended Updates form displays a list of all the update actions that are currently in a 
suspended state. This form also allows you to take selected updates out of suspension manually. 
For more information about this form, see the online help for the form.

### Chapter 5: Event Messages (page 57)

example, a prompt might include buttons or links labeled: 
z
Approve / Disapprove (default option) 
z
Yes / No 
z
OK / Send More Info / Cancel

To customize the choices for a prompt, you must include a Prompt action with a Choices parameter 
as part of the event action definition. This Choices parameters consists of the CHOICES function 
followed by a string expression that evaluates to a comma-separated list that contains an even 
number of elements (value/label pairs). For example, if you want the voting buttons to be labeled Yes 
and No, with corresponding values returned to the action to be 1 and 0, you could include this 
parameter: 
CHOICES("1,sYes,0,sNo") 
In this example, the strings "sYes" and "sNo" are WinStudio form strings. These have already been 
defined for the system as Yes and No, respectively. 
If you want your button labels to be localized, for the recipient, you must: 
z
Use names of existing form strings (as found in the Strings table). 
OR 
z
Add your own form strings, using the Strings form, and provide the necessary translations. (To 
open the Strings form, you must be in Design Mode and, from the Edit menu, select Strings.) 
If localization is not an issue, you can also use a literal value that displays on the button verbatim. To 
specify the string as a literal value here, simply specify it as a list value. If the system does not find the 
string in the Strings table, the system automatically treats it as a literal value. 
See “Event action parameters” on page 126. 
Voting rules 
When a prompt is sent to a single recipient, the result of the prompt is the return value from that 
recipient's choice. However, when a prompt is sent to multiple recipients, you must select a vote-
counting method to determine the result of the prompt and include a Voting Rule parameter in your 
event action definition.

This table lists and describes the available voting rules.  
Rule 
Description 
Majority 
A choice must receive more than 50% of the vote to win. 
As soon as more than 50% of the recipients respond with a 
particular choice, that choice wins. 
If you use this voting rule, you should use a Voting Tie parameter 
(VOTINGTIE) to tell the system how to handle a tied vote. 
See “Dealing with indeterminate voting results” on page 65. 
Plurality 
The choice with the highest number of votes wins, even if it does 
not receive more than 50% of the vote. 
For example, if three choices are offered, and: 
The first choice receives 24% of the vote; 
The second choice receives 43% of the vote; and 
The third choice receives the remaining 33% of the vote; 
the second choice wins, even though it received less than 50% of 
the total vote. 
If you use this voting rule, you should use a Voting Tie parameter 
(VOTINGTIE) to tell the system how to handle a tied winning vote. 
See “Dealing with indeterminate voting results” on page 65. 
ConditionalPlurality 
The choice with the highest number of votes wins, but only if a 
specified minimum percentage of votes is reached. 
If you use this rule, you must also include a Minimum Percentage 
(MINIMUM) parameter. 
For example, if three choices are offered to 19 recipients, and you 
specify a minimum of 40% to win, then: 
In an 8-7-4 split, the choice with 8 votes would win because it 
meets the minimum percentage. 
In a 7-6-6 split, there would be no winner, because no choice meets 
the minimum percentage. In this case, the system must deal with 
the vote as an indeterminate result. 
See “Dealing with indeterminate voting results” on page 65. 
(In contrast, with a simple Plurality vote, the choice that reaches 7 
votes in a 7-6-6 split would win.) 
If you use this voting rule, you should use a Voting Tie parameter 
(VOTINGTIE) or Voting Disparity parameter 
(VOTINGDISPARITY) to tell the system how to handle the 
indeterminate vote. 
See “Dealing with indeterminate voting results” on page 65.

MinimumCount 
The first choice to reach a specified minimum number of votes 
wins. 
If you use this rule, you must also include a Minimum Count 
(MINIMUM) parameter. 
For example, if three choices are offered to 13 recipients, and you 
specifiy a minimum of 5 votes to win, the first choice to receive 5 
votes automatically wins. 
Note that, as soon as the minimum count is reached, event 
execution moves immediately to the next action. In this case, the 
system expires any responses not yet received, and no further 
voting can take place. 
MinimumPercentage 
The first choice to receive a specified percentage of the vote wins. 
The percentage is based on the number of recipients of the prompt, 
not the number of respondents. 
If you use this rule, you must also include a Minimum Percentage 
(MINIMUM) parameter. 
Note that, as soon as the minimum percentage is reached for a 
choice, event execution moves immediately to the next action. In 
this case, the system expires any responses not yet received, and 
no further voting can take place. 
EarliestResponse 
The first response to the prompt wins, regardless of the choice. 
Note that, as soon as the first response is received, event 
execution moves immediately to the next action. In this case, the 
system expires any responses not yet received, and no further 
voting can take place. 
PreferredChoice 
If any one respondent votes for the preferred choice, that choice 
wins. In a case where none of the respondents select the preferred 
choice, then this rule behaves like the Plurality rule for the 
remaining choices. 
If you use this rule, you must also include a Preferred Choice 
(PREFCHOICE) parameter to specify which choice is the preferred 
choice. 
For example, if you have three choices, and you specify the first 
choice as the preferred choice, then: 
If anyone votes for the first choice, that choice wins. 
If the end vote is a 0-6-5 split, the second choice wins. 
Note that, as soon as the preferred choice receives a vote, event 
execution moves immediately to the next action. In this case, the 
system expires any responses not yet received, and no further 

### Appendix A: Sample Scenarios (page 67)

Appendix A: Sample Scenarios
This appendix presents a number of typical scenarios in which you might want to use the Application 
Event System to automate various tasks in response to various situations. In each case, the situation 
is described and then a proposed solution involving events, handlers, and/or triggers. These solutions 
are presented in a step-by-step format, as examples that you can learn from and possibly modify for 
your own use.
Note: 
z
To a certain extent, each scenario builds on the concepts and practices of previous scenarios, so 
the most effective way to use them is to work through them sequentially. However, each scenario 
is also more-or-less "self-contained" and can be used independently of the others. 
z
To see a graphical representation for each flow as you work on it, you can use the Diagram 
button on the Event Handlers form. This button opens the Event Handler Diagram form, which 
you can use to view the flow of the event handler as well as access the Event Actions form to 
edit individual actions. For more information, see the online help for the Event Handler Diagram 
form. 
This list is a list of the scenarios included in this appendix: 
Sending notifications 
z
Scenario 1: Notification of a new record—adding a user on page 68 – A simple notification is 
sent to a credit manager when a new customer is added to the database. 
z
Scenario 2: Notification of changes to an existing record—changing the credit limit on page 74 
– The credit manager is notified by e-mail that a customer’s credit limit has been changed and 
is told what the new credit limit is. 
z
Scenario 3: Notification that includes an "old" value on page 78 – A group of inventory 
stockers are automatically notified whenever an item’s lot size changes. In the message that 
is sent, both the previous lot size and the new lot size are included.
Requesting approvals 
z
Scenario 4: Approval for a new record on page 84 – A purchasing manager is prompted for 
approval whenever a new purchase order is requested.

z
Scenario 5: Requesting approval by external e-mail for changes to an existing record on page 
90 – A credit manager is prompted through an external e-mail for approval of a change to a 
customer’s credit limit. 
z
Scenario 6: Requesting multiple and complex approvals on page 97 – A purchasing manager 
is prompted for approval on a purchase order (PO) both of a change in status to Ordered and 
for the amount of the PO. If the PO is for an amount greater than $100,000, a supervisor is 
also prompted for approval. If the PO is for an amount greater than $1,000,000, two senior-
level executives must also approve it. 
Modifying records 
z
Scenario 7: Adding information to a record on page 109 – A credit manager is prompted to 
provide a credit limit for a new customer, by means of a response to a message. 
Voting
z
Scenario 8: Voting for various choices on page 111– Several managers are prompted to 
approve an engineering change, by means of a response to a message. 
Localizing message contents
z
Scenario 9: Translating captions in a purchase request on page 113 – A message containing 
localizable strings is created. 
More advanced scenarios 
z
Scenario 10: Opening a session in a remote environment on page 115 – A remote site or 
Mongoose environment is accessed to retrieve data. The details of and procedure for this 
scenario are in the Integrating IDOs with External Applications guide. 
z
Scenario 11: Cross-site event firing - adding a message to another site's Inbox on page 116 – 
A message is sent to another site’s Inbox form by using a GenericNotify event.
Sending notifications 
One of the simplest uses of the event system is to set up situations in which message notifications are 
sent out automatically to specified individuals whenever a situation occurs or a condition is met. The 
scenarios in this section illustrate this kind of situation. 
Scenario 1: Notification of a new record—adding a user 
Suppose you have a system administrator who wants to be notified whenever a new user is added to 
the system, regardless of who adds the user. Of course, you can simply require each employee who

adds users to the system to manually send a notice whenever a user is added. But that places an 
additional burden on the employee and is prone to possible oversight. 
A simple event and handler 

added. In this example, you do not need to create an event, because Infor provides an event named 
IdoPostItemInsert that you can use. All you need to do is create an event handler for that event and 
assign an action to it that generates and sends the message to the system administrator. 
We could use the IdoOnItemInsert framework event instead of the IdoPostItemInsert event. This will 
be significant when we get to the section on  Refining the message on page 71. The advantage of 
using the IdoPostItemInsert event is that, if you allow the Users form to auto-assign the user ID 
number (instead of specifying the user ID number yourself), the system waits until the ID number has 
been assigned before filling in the "CustNum" data in the message. If we use the IdoOnItemInsert 
event, the system does not wait, which means that, if you auto-assign the customer ID number, the 
restulting message has "TBD" in place of the actual customer number. 
To set this up: 
1.
Create the event handler: 
a.
Open the Event Handlers form. 
b.
Press F3. 
c.
Press Ctrl+N. 
d.
Create the handler with these settings:  
Field or Option 
Setting / Comments 
Event Name 
From the drop-down list, select IdoPostItemInsert. 
Note: For details about this and the other 
framework events included with the system, see 
“Framework events” on page 122. 
Applies to Initiators 
Leave blank. 
Applies to Objects 
Specify SLCustomers. 
To determine what object you need, see the 
procedure provided in the online help for this field. 
Keep With 
Leave blank. 
Chronology 
Leave blank. 
Ignore Failure 
Cleared. 
Suspend 
Cleared.


### Appendix B: Reference Tables (page 119)

details about the associated event action parameters, including their syntax and examples, see 
“Event action parameters” on page 126. 
WinStudio includes a variety of action types for use when defining event actions. These action types 
are predefined to perform their specified actions when the required parameters are provided. 
In every case, WinStudio includes special event action forms for each event action. These forms are 
designed to help you more easily set up the required and optional parameters for their respective 
event actions. For more information, see the online help for the desired event action form. 
Note: Adjourning event action types (that is, Prompt, Wait, and Sleep) cannot be assigned to event 
actions on a transactional event handler. For more information about adjournment, see “Adjournment 
and resumption” on page 21. For more information about transactional event handlers, see 
“Transactions” on page 24. 
Note: Mid-tier event action types (that is, Call IDO Method, Dispatch IDO Request, Execute IDO 
Request, Load Collection, Load IDO Row, and Update Collection) cannot be executed on a 
synchronous event handler whose event is fired from the database layer (that is, via FireEventSp, or 
attached to any Session framework event).  If this is attempted, the handler fails with an error. 
Event action parameters 
The information formerly located in this section is now available only in the online help. See the topic 
for the parameter you are interested in or use context-sensitive help options. 
Expressions and functions 
Many event action parameters make use of multi-part expressions when performing their various 
operations. These expressions can almost always be constructed with the Event Action Expression 
Editor. which is a versatile tool that provides many options designed to help you build the parameter 
expressions you need without having to actually write code. 
To help in the construction of event action parameter expressions, WinStudio provides a large number 
of standard expression functions, which are all available in the Event Action Expression Editor. 
When selected, each function provides in the editor itself a sample of the correct syntax and a brief 
description. Many functions have more complete descriptions and examples in the online help.

Pre-parser functions 
In addition to the standard expression functions listed in the Event Action Expression Editor, there 
are two “pre-parser functions” that you can use to build expressions: 
z
TGC: Retrieves the value of an event global constant for which the value can contain other 
grammar elements. 
z
TV: Retrieves the value of an event variable in which that value can contain other grammar 
elements. 
These additional functions can be used to expand an event variable or event global constant textually, 
that is, with no assumptions about the structure or data-type of the contained value. These functions 
are useful in cases where the expanded value contains other grammar elements that must be further 
evaluated, for example, to share common expressions, expression elements, or groups of functions. 
When an event action begins, WinStudio first evaluates all TV( ) references recursively, until no more 
references to known variables remain. Next, WinStudio evaluates all TGC( ) references recursively, 
until no more references to known global constants remain. Finally, the resulting parameters string is 
passed to the parser to evaluate all other functions and operators contextually using the grammar 
found in Appendix C, Expression Grammar. 
Simple expansions 
Consider this parameters string: 
Assume that the system is using this event global constant metadata:  
The effective parameters passed to the event system parser would be: 
CONDITION(DATEDIFF(day, BEGINDATE( ), CURDATETIME( )) > 7) TO(USERNAME( )) 
SUBJECT("Old Handler Alert") QUESTION("Do you really want to continue this 
old Handler?") CHOICES("1,sYes,0,sNo") 
Complex expansions 
More complex expansions are possible. For example: 
GC(MyVarTV(VarSuffix)) 
CONDITION(TGC(Over1WeekOld)) TGC(OldHandlerPromptParms) 
Name 
Value 
Over1WeekOld 
DATEDIFF(day, BEGINDATE( ), CURDATETIME( )) > 7 
OldHandlerPromptParms 
TO(USERNAME( )) SUBJECT("Old Handler Alert") 
QUESTION("Do you really want to continue this old 
Handler?") CHOICES("1,sYes,0,sNo")

In this example, first, the value of the current event handler's "VarSuffix" variable is retrieved. Then 
that value is appended to the name "MyVar" to construct an event global constant name, for which the 
value is then retrieved. 
The value of the "VarSuffix" variable might be set dynamically by an event action on the handler, or it 
might be included in different event initial states that are linked from referring handlers, in which case 
the GC( ) reference itself could be moved to its own global constant and referred to from all actions of 
the handlers using TGC( ). 
Note that no operator or other syntax is used around the TV( ) reference, because it is evaluated and 
substituted in-place textually, without regard to data type or context. 
Nested expansions 
Nested expansions are also possible. For example, consider this parameters string: 
TGC(MarkItUp) 
Assume that the system is using this event global constant metadata:  
This has the effect of increasing the value of the "Price" variable by 10% plus 5, but only if the 
resulting value is less than 100. 
Expression operators 
Expression operators can be either unary or binary, meaning they can operate on either one or two 
expressions. Most operators are limited as to what kind of expressions they can operate with. The 
kinds of expressions possible include: 
z
Scalar expressions (scalarExpr) – These expressions can be either of a known type (numeric, 
string, or date) or an unknown type (typeless). 
In the table below, if the expression type is given as scalarExpr, it can be any of these four types. 
z
Numeric expressions (numericExpr) – These expressions evaluate using numeric values. These 
are the expressions used to perform mathematic operations. If a string or typeless expression is 
supplied where a numeric expression is expected, it is automatically converted into a numeric 
value. If that is not possible due to the presence of non-numeric characters, the current handler 
fails with an error. 
z
String expressions (stringExpr) – These expressions are text-based sets of characters. They may 
include numbers, but if so, the numbers are treated as text characters, not numerals. If another 
Name 
Value 
StdMarkup 
* 0.1 + 5 
MarkItUp 
CONDITION(V(Price)TGC(StdMarkup) < 100) 
SETVARVALUES(Price=Price TGC(StdMarkup))

type of expression is supplied where a string expression is expected, it is automatically converted 
into a string representation.
z
Date expressions (dateExpr) – These expressions involve dates or parts of dates, including times 
such as 10:00 AM. 
z
Typeless expressions (typelessExpr) – These are expressions that could be one of at least two 
different types. The way the system treats these expressions depends on the context in which the 
expression is used. 
z
Boolean expressions (BooleanExpr) – These expressions consist of an OR conjunction of one or 
more AND conjunctions. 
To construct the expressions used in “Event action parameters” on page 126, you can use the 
expression operators in this table in conjunction with the “Expressions and functions” on page 126  

### Appendix C: Expression Grammar (page 131)

For example, this produces a parsing error: 
V(this)=1 and 2=V(that)) and 1=(2) 
Instead, you can write it like this, to work around the grammar limitation: 
V(this)=1 and 2=V(that) and 1=2 
z
Operation chains containing a mix of typed and typeless arguments must begin with a typed 
value. 
For example, this example produces an error because the first argument is not a typed value: 
'12'=V(a)+'B'+V(c) 
Instead, and because string concatenation is not commutative, you can write it as: 
'12'=''+V(a)+'B'+V(c) 
Alternatively, you can declare the type for the first argument as: 
'12'=CAST(V(a) AS STRING)+'B'+V(c) 
Again, this example produces an error because the first argument is not a typed value: 
12>V(b)+1+5 
Instead, you can write the expression in one of these ways: 
12>0+V(b)+1+5 
12>CAST(V(b) AS NUMBER)+1+5 
12>1+V(b)+5 
The last solution works because numeric addition is commutative. 
z
Functions cannot be used for variable, parameter, or constant names. 
For example, because the letter y is an abbreviation for year in the DATEPART( ) and 
DATEDIFF( ) event functions, this expression produces an error: 
y = 5 
Instead, you can declare y as yVar. This expression does not produce an error. 
yVar = 5 
Start symbol 
"Start Symbol" = <functionParenList>

Character sets 
This table lists and describes the acceptable characters for elements of the code described. You can 
include any amount of white space between elements. 
{ID Head} = {Letter} + [_] 
{ID Tail} = {Alphanumeric} + [_] + ['['] + [']'] + [.] 
{String Ch 1} = {Printable} - ["] + {LF} + {CR} 
{String Ch 2} = {Printable} - ['] + {LF} + {CR} 
Terminals 
String constants are constructed using one of these rules. The string can be: 
z
Enclosed in double-quotes, containing no double-quote characters as illustrated by this example: 
StringLiteral = "{String Ch 1}*" 
z
Enclosed in double-quotes, containing paired double-quotes that are each interpreted as a single 
embedded double-quote character as illustrated by this example: 
StringLiteral = "(""|{String Ch 1})*" 
This 
Designates 
Number 
The set of numerals: 0123456789 
Letter 
The set of all uppercase and lowercase letters: 
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ 
Alphanumeric 
The set of all characters listed as part of the Number and 
Letter sets 
Printable 
The set of all standard characters that can be printed 
onscreen. This includes the characters from  #32 to #127 and  
#160 (nonbreaking space). The nonbreaking space character 
is included because it is often used in source code. 
Whitespace 
The set of all characters that are normally considered "white 
space" and ignored by the parser. The set consists of: 
z A space (regular) 
z Horizontal  tab 
z Line feed 
z Vertical tab 
z Form feed 
z Carriage return 
z Nonbreaking space

z
Enclosed in single-quotes, containing no single-quote characters as illustrated by this example: 
StringLiteral = '{String Ch 2}*' 
z
Enclosed in single-quotes, containing paired single-quotes that are each interpreted as a single 
single-quote character as illustrated by this example: 
StringLiteral = '(''|{String Ch 2})*' 
Each string constant in an expression or parameter list can be constructed using any of these rules, 
independently of other string constants. 
Integer constants contain no decimal point: 
IntegerLiteral = {Digit}+ 
Real constants contain a decimal point: 
RealLiteral = {Digit}+.{Digit}+ 
Identifiers (variable, constant, and event parameter names) must begin with a letter or underscore, 
and continue with zero or more alphanumeric characters and/or underscores: 
Id = {ID Head}{ID Tail}* 
Rules
Variable, constant, and event parameter references 
<IdValue> consists of one of these: 
V(Id) 
GC(Id) 
SV(Id) 
E(Id) 
<FilterIdValue> consists of one of these: 
FV (Id) 
FGC (Id) 
FSV (Id) 
FE (Id)

Expressions 
A scalar expression is either of a known type (Number, Date, or String), or its type is unknown. 
<Scalar Exp> consists of one of these: 
<Numeric-castable Exp> 
<Date Exp> 
<String Exp> 
<Typeless Exp> 
A numeric-castable expression is either Number, String, or an unknown type.
<Numeric-castable Exp> consists of one of these: 
<Numeric Exp> 
Boolean rules 
A Boolean expression is an OR-conjunction of one or more AND-conjunctions. 
<Boolean Exp> consists of one of these: 
<And Exp> 
<And Exp> OR <Boolean Exp> 
An AND expression is an AND-conjunction of one or more negatable predicates. 
<AND Exp> consists of one of these: 
<Not Exp> 

### Appendix E: Synchronization of Metadata (page 159)

different owners, and provides a number of detailed examples. 
Overview and rationale 
Application event system metadata can come from three primary sources: 
z
The Infor system framework (Mongoose) 
z
Applications produced by Infor and/or Infor’s business partners or other authorized vendor 
developers 
z
End-customer development 
The ownership for the metadata from each of these sources is controlled by the Access As identifier. 
For more information on this identifier, see “About the Access As identifier” on page 31. 
Any of these sources can upgrade and reissue their metadata at times independent of the others. The 
upgrade process must: 
z
Update any changed handlers that they own. 
z
Insert any new handlers they might have created since the last version. 
z
Maintain other owners’ handlers and the relationships between them. 
Therefore, a synchronization mechanism is needed, to make sure that changes by one metadata 
owner do not adversely affect the functioning of another owner’s metadata. 
This mechanism is provided in two components: 
z
The Access As identifier (see “About the Access As identifier” on page 31) 
z
The App Metadata Sync and App Metadata Transport utilities, which both provide the capability to 
synchronize event metadata belonging to different owners. 
Using these utilities, you can export your events and event handlers and make them available for 
import by other metadata owners. You can also use these utilities to import your own or others’ 
metadata into your system. 
For more information about these utilities, see the online help for each utility.

The inherent hierarchy of metadata 

however, an inherent hierarchy, based on the normal production flow and use of the system software. 
As illustrated in this diagram, Infor’s framework developers are the first to develop event system 
objects. Other Infor application developers then can add their own event system objects, as can 
authorized business partners and other vendor developers. Finally, end customers can make custom 
modifications and develop their own custom event system objects.  
In reality, the system is designed so that no metadata owner can modify or delete the metadata of 
another owner. So, in that sense, they are all equal. However, this real-time production flow creates 
an inherent hierarchy that allows us to think of them as "higher-level" (that is, Infor) and "lower-level" 
(that is, end-customer) owners. 
With that in mind, we can state these general rules: 
z
Lower-level owners can insert their handlers between two higher-level handlers for the same 
event. 
z
In many cases, lower-level owners can override higher-level handlers. 
There is, however, an option for higher-level owners to disallow overrides for individual handlers. 
z
Higher-level handlers that are overridden remain in the metadata store but are marked as 
Inactive. 
This means, among other things that, if the lower-level handler is later deleted, the higher-level 
handler is still available and can become active again. 
Chronology rules allow downstream owners to integrate and control the sequence of their events and 
handlers with respect to those upstream. For more information, see “Detailed examples” on 
page 161.

Maintaining handler IDs through metadata updates 
Each event handler is identified with a unique (and hidden) ID, which is referenced by the Keep With 
field on the Event Handlers form. This ID, rather than the actual Handler Sequence number, 
becomes the "fixed" reference point for that handler. This means that an event handler owner does 
not need to worry about maintaining the Handler Sequence numbers across releases: The system 
takes care of it automatically, by preserving the hidden ID number and reassigning Handler 
Sequence numbers as required. 
After each insertion, update, or deletion of a handler, and during a merge performed by the App 
Metadata Sync utility or the App Metadata Transport utility, the system calculates new integers, if 
necessary, for display in the Handler Sequence field. The underlying ID, however, remains 
unchanged. When a handler is deactivated and another added in the same position, the new handler 
gets a new ID. 
Protecting running events from metadata changes 
Once an event handler begins executing, it is essential to prevent changes to its attributes and 
actions. Otherwise, unpredictable behavior could result, especially if actions are resequenced. 
One way to prevent these changes would be to make a copy of all active, non-obsolete handlers and 
their actions each time an event is triggered and control execution from this copy. However, that 
method would result in the persistence of a great number of identical copies, assuming that handlers 
are modified much less frequently than they are executed. 
Since the system stores state data separately from metadata, it is sufficient to make a copy only when 
the metadata changes, and furthermore only when the corresponding event is triggered and a copy of 
the last metadata modifications has not yet been made. 
In other words, handler metadata for an event can be created and edited as many times as 
necessary. The first time the event is triggered, a copy of the last saved metadata is made. This copy 
is called an event revision. The execution of the event's handlers is then controlled by the event 
revision and not by the original metadata (which happen to be identical at this point). 
The event can be triggered as many times as necessary, all the time controlled by this event revision, 
as long as no intervening modifications have been made to the original metadata. 
After one or more metadata edits have been saved, though, the next time the event is triggered, the 
system copies a new event revision from the last-saved metadata. 
For more information about event revisions, see “Events and event handler revisions” on page 28. 
Detailed examples 
This section provides three detailed examples of how sequencing and synchronization work in the 

Using specific chronology 
The primary way for a lower-level handler creator to resequence existing handlers (from higher-level 
owners) is to use what is known as specific chronology. That is, the handler’s creator can attach the 
new handler to an existing handler and specify the order in which the two handlers are to execute with 
respect to each other. 
The mechanism used to do this are the Keep With and Chronology fields on the Event Handlers 
form. These fields allow you to specify whether your handler should run before, after, or in place of the 
handler it is associated with, as in this example. 
For more information about the Keep With and Chronology fields, see the online help for those 
fields. 
Infor creates a framework event with three handlers 
The Infor framework team creates an event, FrameEvent, and creates three event handlers that 
execute in order when the event is generated. 
This event and these handlers are all included with the application software when it ships. 
Note that, if a "lower-level" developer wants to add or modify handlers, these rules apply: 
z
Lower-level handler creators cannot change the sequence of higher-level handlers. 
z
Any handlers lower-level creators want to use that will affect the sequence in specific ways 
must be associated with a particular, already-existing handler, using the Keep With and 
Chronology fields.

A business partner creates an additional handler 
An Infor business partner decides to add a handler that will execute just after the first framework 
handler. The business partner creates the event handler and uses the Keep With and 
Chronology fields to keep their handler with ID 1 (S1) and to execute After that handler. 

### Appendix F: Event Flow Options (page 187)

examples of use 1-10
flow diagram F-187
how it works 2-13
overview 1-7
Application events B-125
application-specific events 3-32
asynchronous
event handlers 2-16
events 2-17
events in transactions 2-26
authorization group for event system forms 3-43, 
4-53
B
BodOnReceive B-122
Boolean rules for expressions C-135
C
Caption, in Inbox form 5-59
complex expansions of functions B-127
ConditionalPlurality voting rule 5-63
constants, event global 3-42
controlling
ownership of metadata 3-31
sequence
event actions 2-14, 3-48
event handlers 2-14, 3-47
core (framework) events B-122
Core events 3-32
creating
event actions 3-37
event global constants 3-42
event handlers 3-36
event triggers 3-34
events 3-33
custom events and handlers 3-31– 3-51
designing custom events 3-46
setting up 3-45
customer-defined events 3-32
D
date expressions, rules C-146
defining
event actions 3-37
event global constants 3-42
event handlers 3-36
event triggers 3-34
events 3-33
design forms 3-43

Access As 3-31
authorization group for 3-43
Event Actions 3-37
Event Global Constants 3-42
Event Handlers 3-36
Events 3-32
location 3-43
designing custom events and handlers 3-31– 3-51
disabling event handlers
individually 2-15
with Session Access As 2-15
E
EarliestResponse voting rule 5-64
elements of the application event system 3-31
enumerations C-154
event action parameter forms 3-40
event actions 3-37
controlling sequence 2-14
defining 3-37
parameters B-126
setting sequence order 3-48
Event Actions form 3-37
Event Global Constants form 3-42
Event Handler Revisions form 4-55
Event Handler Status form 4-54
event handlers 3-36
controlling sequence 2-14
defining 3-36
designing custom 3-46
disabling individually 2-15
disabling with Session Access As 2-15
restricting which run 2-14
revisions 2-28
setting sequence order 3-47
setting up custom 3-45
status of
Failure 2-22
Success 2-21
success, failure, and retries 2-21
suspending 2-18
synchronicity (summary) B-121
synchronous and asynchronous 2-16
transactional 2-25
Event Handlers form 3-36
event messages 5-57– 5-66
indeterminate voting results 5-65
prompts and responses 5-61
related forms 5-57
voting rules 5-62
event queue
Framework Event Service 2-27
processing order 2-27
Event Queue form 4-54
Event Revisions form 4-55
Event Status form 4-53
event triggers 3-34
defininig 3-34
retesting 3-35
setting conditions for 3-35
Event Triggers form 3-34
Event Variable Groups form 3-41
event variables 3-41
events 3-32
action types B-126
actions 3-37
asynchronous 2-17

defining 3-33
firing from tiers B-120
flow diagram 2-13
framework (core) B-122
global constants 3-42
handlers 3-36

---

## Full Chapter Extraction

Complete text extracted from each chapter of the AES Guide.

### Front Matter
*Pages 1-2*

Infor Mongoose 
Guide to the Application Event 
System
Copyright © 2015, Infor
Important Notices 
The material contained in this publication (including any supplementary information) constitutes and 
contains confidential and proprietary information of Infor.
By gaining access to the attached, you acknowledge and agree that the material (including any modi-
fication, translation or adaptation of the material) and all copyright, trade secrets and all other right, 
title and interest therein, are the sole property of Infor and that you shall not gain right, title or interest 
in the material (including any modification, translation or adaptation of the material) by virtue of your 
review thereof other than the non-exclusive right to use the material solely in connection with and the 
furtherance of your license and use of software made available to your company from Infor pursuant 
to a separate agreement, the terms of which separate agreement shall govern your use of this mate-
rial and all supplemental related materials ("Purpose").
In addition, by accessing the enclosed material, you acknowledge and agree that you are required to 
maintain such material in strict confidence and that your use of such material is limited to the Purpose 
described above. Although Infor has taken due care to ensure that the material included in this publi-
cation is accurate and complete, Infor cannot warrant that the information contained in this publication 
is complete, does not contain typographical or other errors, or will meet your specific requirements. 
As such, Infor does not assume and hereby disclaims all liability, consequential or otherwise, for any 
loss or damage to any person or entity which is caused by or relates to errors or omissions in this 
publication (including any supplementary information), whether such errors or omissions result from 
negligence, accident or any other cause.
Without limitation, U.S. export control laws and other applicable export and import laws govern your 
use of this material and you will neither export or re-export, directly or indirectly, this material nor any 
related materials or supplemental information in violation of such laws, or use such materials for any 
purpose prohibited by such laws.
Trademark Acknowledgements
The word and design marks set forth herein are trademarks and/or registered trademarks of Infor 
and/or related affiliates and subsidiaries. All rights reserved. All other company, product, trade or ser-
vice names referenced may be registered trademarks or trademarks of their respective owners.
Publication Information
Release: Infor Mongoose 9.02
Publication date: October 20, 2015

### Chapter 1: About the Application Event System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .7
*Pages 3-3*

Contents

Example 1: Sending a notification when a record is added . . . . . . . . . . . . . . . . . . . . . . . . . .10
Example 2: Getting approval for a credit limit change . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .10
Example 3: Complex approval of a purchase order status change . . . . . . . . . . . . . . . . . . . .11
Example 4: Automatically shipping a customer order. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11
Workflow event handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .12

How events are handled. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
When events can be generated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13
Where events can be generated  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Controlling the sequence of event handlers and actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Restricting which handlers run . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14
Using event handler settings  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Using the Session Access As form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15
Synchronicity  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Synchronous events. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16
Asynchronous events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17
Suspension. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18
When an event is not suspended . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Payload  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20
Adjournment and resumption . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success, failure, and retries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21
Success . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21

### Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31
*Pages 4-4*

Failure. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .22
Retrying event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23
Transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .24
Transactions with synchronous events. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .24
Event handlers marked Transactional . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .25
Event handler not marked Transactional . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .26
Rolling back transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .26
The Framework Event Service . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Setting up the Framework Event Service . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Processing order in the Framework Event Service  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27
Administrative details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28
Events and event handler revisions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28
Chapter 3: Designing and Using Events and Handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31

About the Access As identifier . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31
About events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .32
About event triggers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .34
About event handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .36
About event actions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .37
About event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .38
About event action parameter forms  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .40
About event variables and initial states  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .41
About event global constants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .42

Setting up custom events and handlers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .45
Designing a custom event  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .46
About event handling and order . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .47
Determining names of IDO collections and components . . . . . . . . . . . . . . . . . . . . . . . . . . . .48
Refreshing the metadata cache . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .50
Chapter 4: Tracking Event System Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .53
Event Handler Status form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Queue form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .54
Event Revisions form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55
Event Handler Revisions form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55

### Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
*Pages 5-5*

Suspended Updates form. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .55
Chapter 5: Event Messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
Event message-related forms. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
The Inbox form. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .57
The Saved Messages form. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .59
The Send Message form  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .60
Sending e-mail to external e-mail Inbox for prompts  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .60
Prompts and responses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .61
Voting rules. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .62
Dealing with indeterminate voting results. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .65
Quorums. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .66
Appendix A: Sample Scenarios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
Sending notifications  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .68
Requesting approvals. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .84
Modifying records . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .109
Voting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .111
Localizing message contents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .113
More advanced scenarios  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .115
Appendix B: Reference Tables. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
Firing events . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .120
Summary of synchronous functionality. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .121
Framework events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .122
Application events  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .125
Event action types  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Event action parameters. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Expressions and functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .126
Pre-parser functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .127
Expression operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .128
Appendix C: Expression Grammar  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Restrictions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Start symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .132
Character sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133

### Appendix D: Sample Stored Procedures. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157
*Pages 6-6*

Terminals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .133
Rules  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .134
Variable, constant, and event parameter references . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .134
Expressions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .135
Boolean rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .135
Typeless rules  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .138
String rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .140
Numeric rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .143
Date rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .146
Restricted arguments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .154
Keyword paren lists  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .154
Enumerations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .154
Appendix D: Sample Stored Procedures. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157
Passing parameters to a synchronous event . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .157
Calling a synchronous event within a transaction and handling failure  . . . . . . . . . . . . . . . . . . .157
Appendix E: Synchronization of Metadata . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159
Overview and rationale. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .159
The inherent hierarchy of metadata . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .160
Maintaining handler IDs through metadata updates. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Protecting running events from metadata changes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Detailed examples  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .161
Using specific chronology. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .162
Using non-specific chronology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .165
Performing upgrades . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .173
Overriding others’ handlers  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .177
Non-exclusive overrides . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .178
Exclusive overrides. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .180
Disabling the ability to override. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .182
Dealing with obsolete handlers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .182
Appendix F: Event Flow Options . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
Glossary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
Index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 197

### Chapter 1: About the Application Event
*Pages 7-12*

Chapter 1: About the Application Event 
System

customize how the system works. You can use these tools to define and monitor events across the 
system, rather than being limited to a single form. 

z
Events are uniquely named incidents that can occur during the use of an application. Events can 
have multiple triggers and can be generated by user actions, conditions in a database, other 
events, or other situations. 
z
Event handlers consist of data that specifies: 
z
The events to which they are to respond 
z
Any conditions, situations, or attributes that determine when and why each handler executes 
z
One or more event actions to take place during the handler’s execution 
Each event can have multiple handlers but each handler can be associated with only one event. 
z
Event actions consist of instructions that specify the individual tasks or bits of work that are 
performed by the event handler. Each event handler must have at least one action and can have 
multiple actions. 

This diagram is an example of one possible set of events, event handlers, and event actions.  
For example, you might want the system to automatically notify you whenever someone adds a 
customer order to the system and to request your approval if the order is $1000 or more. In this 
example: 
z
The event in this case gets triggered whenever someone creates a new customer order. 
z
The event and the situation that tells the event handler to run are set up as part of the event 
handler definition. 
z
The event action that you want to take place is a notification that an order has been placed. You 
also want that event action to request approval for orders of $1000 or more. 
z
Only a single event handler is needed here. But that event handler requires several actions to 
complete all the requirements: 
z
The first action must check the amount of the order and determine, on the basis of the 
amount, what additional actions are required. If the order is $1000 or more, then it must direct 
the flow to another action that requests a manager’s approval. If the order is less than $1000, 
then it directs the flow to a different action that simply sends out a notification that the order 
has been placed. 
z
The second action is used only if the order is $1000 or more. If this action is used, the system 
generates a prompt message to the manager, requesting approval for the order. The system 
then waits until the manager responds. If the manager approves the order, the system then 
proceeds to the next action. If the manager does not approve the order, the event handler fails 
and no further action is taken. (Though, as good general practice, you should provide for this 
eventuality as well; but, in the interest of keeping this example simple, we will not provide for 
the case where the order is not approved.) 
z
The third action is used regardless of the amount of the order. This action sends out a 
notification to let the manager know that the order has been completed.

Conceptually, the event and associated handlers might look like this:  
For more examples, including the processes to create them, see Appendix A, "Sample Scenarios.” 

Events and event handlers are tagged at the time of their creation with a special identifier (Access As) 
that prevents them from being modified or deleted by other development organizations. Among other 
things, this prevents your custom events and handlers from being overwritten when Infor or another 
developer issues updates to their events and handlers. 

application code to generate events, and for developers and system administrators to create handlers 
for those events. Event handlers can augment or replace the default framework or application 
behavior associated with the event. You can design event handlers so that maximal work can be 
performed without requiring new procedural code. 
This is possible because event handlers are defined using metadata. Metadata, in this context, refers 
to the practice of using uncompiled code and information about data formats that are interpreted 
during run time, rather than compiled code (called here "procedural code").

See Chapter 3, “Designing and Using Events and Handlers.” 

z

performs without having to modify the basic code. Business processes are, therefore, "softer" and 
easier to modify. You can modify application processes and policies without having to directly 
modify the application code and, in many cases, without having to write any procedural code at 
all. This means that the amount of procedural code required to implement functionality can be 
greatly reduced or even eliminated altogether. 
z
You can use your event handlers with events created by others to gain control of the application 
flow and take appropriate action, rather than being forced to call into the application using APIs. 
z
Because event handlers are defined using metadata, there is no upgrade problem, and no 
collision problem if other developers also have event handlers for the same event. 
Examples of ways to use the Application Event 
System 
These examples offer illustrations of how to use the application event system, including explanations 
of how this can benefit you. For more sample scenarios, including the procedures required to 
implement them, see Appendix A, "Sample Scenarios.” 
Example 1: Sending a notification when a record is added 
Suppose you have a sales manager who wants to be notified whenever someone adds a new 
customer to the system. You could rely on personnel compliance by anyone who has the ability to add 
customers to the system and trust them to remember to send the sales manager an e-mail. This, 
however, might not be the most reliable solution. 

can set up an event that is generated whenever anyone adds a new customer into the system, and 
use event handlers and actions to automatically generate a notification that is sent to the sales 
manager. 
For a more detailed example, including the procedure to create and use the required handlers, see 
"Sending notifications" on page 68. 
Example 2: Getting approval for a credit limit change 
Suppose your company requires that any change to a customer’s credit limit be approved by a 
designated credit manager. You could require any customer representative to contact that credit 
manager whenever a change to a credit limit is requested.

manager a message requesting approval of the change. To speed up the process, you can also send 
an e-mail to the credit manager that contains links the manager can click to approve or deny the 
request. 
When the credit manager responds to the message and approves the request, the system can then 
automatically change the credit limit amount. 
For a more detailed example, including the procedure to create and use the required handlers, see 
"Requesting approvals" on page 84. 
Example 3: Complex approval of a purchase order status change 
Suppose your company has a business process in place that: 
z
Requests approval from a purchasing manager when the status of any purchase order (PO) is 
changed to Ordered. 
z
If the purchasing manager approves the request and the total cost of the PO exceeds a certain 
amount, requests majority approval from a group of higher level managers on whether the order 
should be sent to the vendor. 
z
If those managers also approve and the total cost of the PO exceeds another, higher amount, 
requests unanimous approval from a group of top-level directors. 
z
If the request is approved at all the required levels for the total cost of the PO, the transaction is 
approved and completed. 
As with the previous two examples, this process could all be taken care of manually, involving actions 
by many employees. However, the potential amount of time consumed and the risk of something 
getting missed somewhere increases with each approval required. 
So, you could use events and handlers to automate this entire process, evaluating the PO at each 
step of the way, requesting only the necessary approvals, and completing the transaction upon 
approval. 
Example 4: Automatically shipping a customer order 
Suppose you have a system that, by default, requires someone to manually set the system to ship a 
customer order line when the the status of the line is set to Filled. This can cause delays in orders, if/
when the responsible employee does not set the order to ship in a timely manner. 

to ship as soon as the status is set to Filled.

Workflow event handlers 

users, the system can be somewhat overwhelming at first. 
To help you with the learning curve, Infor provides a New Workflow Wizard, which is designed to 

more information, see the online help topic, “Creating Workflows with the Wizard.” 
Some Mongoose-based applications also include a Workflow Event Handler Activation form to 
help non-developers create simple AES workflows. This form provides access to a set of predefined 
workflow event handlers. These handlers are almost ready-to-use; in most cases, all you need to do 
is define the user names or e-mail addresses of the people who should be notified when a certain 
event happens, and activate the handler. For more information, see the application's online help.

### Chapter 2: How the Application Event
*Pages 13-30*

Chapter 2: How the Application Event 
System Works 
Events are generated (or fired) in response to an action or condition that occurs in the system. When 
the event is generated, it can execute one or more event handlers with the event actions associated 
with each event handler. 
How events are handled 
Essentially, when an event is generated, it requires an event handler to do something in response. 
Otherwise, the event serves no practical purpose. That is, if there is no handler for an event, the event 
actually does nothing when it is generated. 
TIP: That does not mean that an event should never exist unless it has an event handler. Infor 
includes some framework events as part of the system. Infor does not include handlers for these 
events. These events were created to provide events that other developers can use with their own 
custom event handlers. 
When events can be generated 
An application event can be generated when: 
z
A system user performs a particular action, perhaps only on a given form and/or when a particular 
business process is involved. 
z
A database calculation is performed, perhaps resulting in a certain value. 
z
Another event results in generating this event. 
z
A certain amount of time has passed. 
These are all examples of situations and conditions that can fire events: 
z
A sales representative saves a record in the Customers form. 
z
A manager changes the credit hold status of a customer. 
z
A factory manager adds a new item to the list of those being manufactured in that facility.

z
The first day of each month arrives. (An event can be used to generate a monthly report, for 
instance.) 
z
The quantity-on-hand of a particular item becomes less than zero. 
Where events can be generated 

z
In the client tier, the event can be generated by using a form that has a form event handler with a 
response type of Generate Application Event. 
z
In the middle tier, the event can be generated by invoking an appropriate .NET method. 
z
In the database tier, the event can be generated by using an appropriate stored procedure. 
z
In any tier, an event can generate another event by using the GenerateEvent action type. 
For details on how to generate an event from any of these locations, see “Firing events” on page 120. 
Controlling the sequence of event handlers and 
actions 
Two types of settings control the order in which event handlers and their actions execute: 
z
Each event handler has a handler sequence number. Handlers execute in the order of their 
sequence numbers. 
To modify the flow and change handler sequence order, use the Keep With and Chronology 
options on the Event Handlers form or the Event Handler Sequence form. 
See “About event handling and order” on page 47. 
z
The event actions associated with each event handler also have their own action sequence 
numbers. These execute in numeric order, unless: 
z
You use the Initial Action option on the Event Handlers form to designate that a particular 
action should execute first. 
z
You use certain event action types to modify the flow. 
See “About event actions” on page 37. 
Restricting which handlers run 
There might be times when you want or need to disable the event handlers created by one or more 
development organizations, including yours, at least temporarily. This would occur typically when you

are troubleshooting problems with the application event system. The system offers two basic ways to 
disable event handlers. 
Using event handler settings 
When you want to disable only certain event handlers temporarily, use the Active check box on the 
Event Handlers form. 
You can only disable (or enable) event handlers that have the same Access As identifier that you 
have. You cannot, for instance, use this technique to disable Core event handlers. 
Using the Session Access As form 
When you want to disable (or enable) all the event handlers created by a particular developing 
organization all at once, you can use the Session Access As form to accomplish this. 
Note: An alternate way to accomplish the same thing for individual handlers with your Access As 
value is to open the Event Handler form and for each event handler that you do not want to include in 
testing or debugging, clear the Active check box. 
An example 
Suppose, for example, that a customer is having a problem that he suspects is being caused by 
something he did in the event system, but he is not sure what. He places a call to Infor technical 
support, and the technical support representative wants to verify that the customer’s custom event 
handlers are not causing the problem. 
In this case, the technical support representative might ask the customer to temporarily disable all 
custom event handlers so that the operation can be tested with only standard functionality in place. 
The technical support representative might instruct the customer to use the Session Access As form 
to perform either of these actions: 
z
In the Include Access As field, specify Core,BaseAppAccessAs where BaseAppAccessAs is 
the Access As identifier associated with the base application installed on the system. 
With this setting, only the Infor core (framework) and base application event handlers will execute. 
Custom event handlers created by the end-customer do not execute. 
See “Session Access As form options” on page 16. 
z
Leave the Exclude Access As field blank, and select the Exclude Blank Access As check box. 
This option allows all Infor and business partners event handlers to operate. Only the customer’s 
event handlers are ignored. 
See “Session Access As form options” on page 16.

Session Access As form options 
To disable or enable event handlers using the Session Access As form, use any of these options: 
Note: You are not obligated to use both the Include Access As and the Exclude Access As fields. 
You can use any combination of the options available on this form. 
z
With the Session Access As form open, in the Include Access As field, specify the Access As 
identifiers for event handlers that are to be recognized during this session. 
To include multiple Access As identifiers, list them separated only by commas (no spaces). 
If this field is left blank, the system can recognize and execute all event handlers. 
z
In the Exclude Access As field, specify the Access As identifiers for event handlers that are to 
be ignored during this session. 
To exclude multiple Access As identifiers, list them separated only by commas (no spaces). 
If this field is left blank, the system can recognize and execute all event handlers. The exception 
to this occurs only if the Exclude Blank Access As check box is selected. In this case, all event 
handlers are recognized except event handlers for which the Access As identifier is null (blank). 
z
To exclude those event handlers that have a blank Access As identifier, select the Exclude Blank 
Access As check box. 
Synchronicity 

of event handlers to run independently from other event handlers. Events are said to be 
“synchronous” when they must execute their handlers in a specific order. Events are said to be 
“asynchronous” when they can execute their handlers independently of other handlers. 
A synchronous event handler is one that must complete before the system continues to the next 
event handler in a sequence. For the entire event to be handled successfully, all synchronous 
handlers in the sequence must complete successfully. The exception to this rule is that, if one event 
handler fails, other than for an illegal operation, and the system is set to ignore failures for that 
handler, the system can continue to the next synchronous event handler. Otherwise, the system 
returns a failure error, and no more event handlers in the sequence execute. 
By contrast, an asynchronous event handler runs independently of other event handlers. 
Synchronous events 
Unless the event is designed to suspend, the expectation is that the event will complete 
synchronously. Therefore, its synchronous event handlers execute in sequence in the same thread 
that generated it and block that thread until they have all been executed or until a handler exits with a 
failure status. 
Events are synchronous when they are generated by:

z
Core (framework) events 
z
Calling the FireApplicationEvent() .NET method with the Synchronous parameter set to True 
z
Calling the dbo.FireEventSp stored procedure 
z
Using a form event handler with a response type of Generate Application Event and the 
Synchronous option selected 
z
Using an event action of the type Generate Event and a parameter of Synchronous(True) 
Asynchronous events 
This means that the event runs in a different thread than the one that posted it, usually on a utility 
server. In this case, the event does not block the generating thread, running independently of it. As 
soon as an acknowledgment is received that the event was successfully queued, the thread that 
generated the event continues on. 
See “The Framework Event Service” on page 27. 
Events are asynchronous when they are generated by: 
z
Calling the FireApplicationEvent() .NET method with the Synchronous parameter set to False 
z
Calling the dbo.PostEventSp stored procedure 
z
Using a form event handler with a response type of Generate Application Event and the 
Synchronous option cleared 
z
Using an event action of the type Generate Event and a parameter of Synchronous with a value 
of False 
Event handlers 
Event handlers can be designated as synchronous or asynchronous at the time they are created, 
using the Synchronous check box on the Event Handlers form. 
Any event, either synchronous or asynchronous, can execute an asynchronous event handler when 
execution reaches an event handler designated as an asynchronous event handler; that is, for which 
the Synchronous check box is cleared. At this point: 
z
The system sends the asynchronous event handler to the event handler queue. 
Called queueing, the system does this by means of the PostEventHandlerSp stored procedure, to 
which it passes the configuration name from the event state. 
z
If queueing was successful, the event's thread continues on to the next event handler or, if no 
subsequent handlers are defined, completes the event. 
z
If queueing was unsuccessful, the event stops with a failure condition. 
See “Summary of synchronous functionality” on page 121.

Suspension 
Suspension occurs when a requested operation is sent to the event system for completion at a later 
time. This occurs when the event handler has the Suspend option selected and contains an 
adjourning action. 
Suspension is possible only with certain framework events. You cannot create custom events that can 
be suspended. Currently, these are the events that can be suspended: 
z
IdoOnItemInsert 
z
IdoOnItemUpdate 
z
IdoOnItemDelete 
Suspension occurs when the system generates an event that: 
z
Is one of these framework events that can be suspended. 
z
Has the Suspend check box selected (on the form) for at least one handler that applies to the 
generated event’s object and initiator. 
When an event is suspended 
When both of the above conditions are met, WinStudio passes control of the requested update 
(insertion/update/deletion) to the application event system. The application event system then tries to 
make sure the event handlers can all execute successfully before actually committing the system 
(and the data) to execution of the event actions. 
This is done in two stages. 
Suspend-validating stage 
When an event is suspended, in what is known as suspend-validating stage, the system: 

Begins a database transaction. 

Performs an update to the database, to validate pertinent data against any SQL constraints or 
triggers. 

Validates the data by running all effective event handlers that are synchronous and not 
suspended in the current transaction. 
This involves both application and event system changes. 
z
At the beginning of this process, in a separate event transaction, the system copies the event 
handler to a new revision, if necessary. 
See “Events and event handler revisions” on page 28. 
The reason for this is that both the suspend-validating mode and the suspend-committing 
mode (described in the next section) must use the same metadata. However, the validating 
transaction will be rolled back, and the master transaction might be rolled back. So, the

current event handler revision must be available, in case someone edits the handlers 
between execution of the two modes. 
z
During this process, a non-output event parameter named Suspend_ValidatingMode with a 
value of 1 is made available to handlers. 

Rolls back the transaction. 

Places a task on the event queue to run all involved handlers in suspend-committing mode 
See “Suspend-committing stage” on page 19. 
If the collection update is rolled back due to a later error, this suspension is also rolled back with it, 
resulting in a state identical to one in which this update was never requested. 
When the event service picks up the queued event, it knows that a suspension is in effect by 
checking the EventQueue.Suspend attribute. 

The system marks the record involved in the update/deletion request to have the InWorkflow 
property set to 1. This prevents any user from attempting another change to the suspended 
record. Note that suspended insertions do not reach the database at all unless and until the 
suspended event finishes successfully. 

The thread in which the event was generated continues on as if the change request succeeded. 
This occurs even if the thread originated from an event handler executing an UpdateCollection or 
ExecuteIDORequest type event action. In other words, suspension affects only one level of event 
execution. 
Suspend-committing stage 
Once the suspended event completes the suspend-validating mode successfully and is placed on the 
event queue, the system processes the event using these rules. This is known as the suspend-
committing stage. 
z
Any failure or error condition prevents further event handlers from executing and prevents the 
standard processing (that is, the requested insertion, update, or deletion) from occurring. 
However, the InWorkflow attribute is cleared. 
z
After each event handler finishes successfully, execution proceeds to the next event handler. 
z
The system queues any asynchronous event handler, and execution proceeds to the next event 
handler. 
z
When the last event handler finishes or is queued successfully: 
TIP: You can test this on any synchronous, non-suspended handlers that you do not 
want to execute at this time (perhaps because its actions would irreversibly affect 
something not controlled by our database transaction), using the expression 
CONDITION( E(Suspend_ValidatingMode)<>1). 
Note: At this point, the event system treats any failure as an error and exits the 
execution of the event. 
NOTE: Suspended records in a workflow are indicated as such by a purple icon in the 
status indicator column of a grid.

z
The standard processing is committed. 
That is, the requested insertion, update, or deletion occurs. 
For an update request, this also includes clearing the InWorkflow attribute. 
z
The event finishes. 
When an event is not suspended 
When an event that can be suspended is not suspended (that is, no event handler for that event that 
applies to that event’s object and initiator has the Suspend check box selected), the system executes 
the event using this process: 

The system performs a database update. 

The event system executes all effective event handlers, returning either success or failure. 

The system handles failures as errors and exits the event. 
Note: Each insertion/update/deletion request in the process—which could be from an external XML 
request or from a Save action in WinStudio—participates in the overall transaction. In this case, all 
complete or nothing completes. So, each handler chain (the same chain executes for each insertion/
update/deletion in the group) also participates in that overall transaction. A failure of any of those 
handler chains results in the entire transaction being rolled back. 
Payload 
In either of the above cases, an event that can be suspended carries a payload that represents, and 
that allows handlers to access and modify, the requested change (that is, insertion, update, or 
deletion).  
Each named property value that forms part of the change is passed into and out of the event system 
as a parameter with a name of the form “Row.Property", where Property is the name of the IDO 
property.  Modified property values are accompanied by another parameter with a name of the form 
"Row.Property.Modified" and a value of “1”.  
During notify and prompt actions, these parameters are: 
z
Temporarily converted to event variables, which overrides any value that might have been set in 
preceding actions or specified on the Event Variable Groups form. 
z
Available for display (and update, for prompts) on the Variables tab of the Inbox form (and for 
display at the end of an external e-mail prompt). 
z
Then converted back to parameters for subsequent actions. 
During other actions such as Set Values, these parameters can be modified to affect the final result of 
the change when it is applied to the database. This can be done by using this syntax:

z
SETPROPVALUES("Property"=expression) – If the new value is different than the original 
framework event parameter received by the event, the PROPERTYMODIFIED(PropertyName) 
framework event parameter is also set to TRUE automatically. 
z
SETPARMVALUES(Row.Property=expression, Row.Property.Modified="1") – Note that you 
should also indicate to the framework that the property is now modified, as shown. 
Adjournment and resumption 
Some chains of event actions might need to be temporarily stopped, while waiting for some condition 
to be met. For instance, a customer order might need a manager’s approval before it can be entered 
into the system. In this case, the system temporarily halts the execution of the event handler chain 
until the condition is met; for instance, until the manager responds with an approval (or not). This is 
known as adjournment. 
Certain event actions, called adjourning actions, must wait for an external stimulus before the event 
handler can proceed with the next action. An event handler containing such an action must be either: 
z
Asynchronous 
OR 
z
Part of a framework event that can be suspended and is marked to suspend. 
See “Suspension” on page 18. 
When execution reaches an adjourning action, the event handler state is set to retest or time out at a 
specified time. At this point, the event becomes an adjourned event. 
The event service then processes it at the next opportunity after the Time Out and/or Retest time. 
This is called resumption. 
Success, failure, and retries 
Each event handler can exit with a status of Success or Failure. When an event handler fails, if it is 
not set to ignore failures, and if it has not attempted an illegal operation, the system can retry the 
event handler’s actions. 
Success 
An event handler exits with a status of Success only when it either: 
z
Reaches an event action of the type Finish. 
OR 
z
Completes all event actions successfully without reaching an event action of type Fail.

Failure 
An event handler exits with a status of Failure when it does any of these: 
z
Reaches an event action of the type Fail. 
z
Attempts an illegal operation. 
z
Experiences an unexpected failure of an event action or something launched by an event action. 
When failures occur 
When a failure occurs: 
z
The Event Handler Status form’s Result field displays an appropriate error message, which 
includes an error message passed from a failing stored procedure in a message type parameter 
(@Infobar), where applicable. 
z
The Times Failed counter for the current event action state is incremented. 
This value displays on the Actions tab of the Event Handler Status form. 
z
The event handler state's Last Activity Date is set to the date and time of the failure. 
This value displays on the Handlers tab of the Event Handler Status form. 
z
Any event variables are maintained at their current values for inspection on the Variables tab of 
the Event Handler Status form. 
Ignoring failures 
By default, if any synchronous event handler reports a failure, the system skips any remaining event 
handlers for that event and exits with a status of Failure. 
You can override this default behavior by using the Ignore Failure option for the event handler (on 
the Event Handlers form). If you select this option, the event handler is always treated as successful 
unless an illegal operation is deliberately attempted. The Status field on the Event Handler Status 
form, however, still shows a status of Failure, even though the Any Handlers Failed check box 
remains cleared. 
This table shows what conditions can result in failures for various action types and whether the failure 
can be ignored.  
Action type for 
the current 
event action 
Condition 
Ignore Failure 
option selected? 
Result 
(Event 
Status) 
Set Values 
Illegal operation: Any attempt to set a 
non-output event parameter 
n/a 
Failure 
Some 
Illegal operation: Any attempt to use 
an action type that is not supported 
on the current tier 
n/a 
Failure

A Fail action whose condition evaluates to True on an event handler for which the Ignore Failure 
option is selected is equivalent to a Finish action. 
An asynchronous event handler's failure does not affect any remaining event handlers for that event. 
However, setting the Ignore Failure option in this case avoids affecting the AnyHandlersFailed() 
attribute of that event, unless the failure was caused by deliberately attempting an illegal operation, 
as shown in the table. 
Retrying event handlers
In the Event Status and Event Handler Status forms, you can retry a failed event handler, if it is 
retryable. Whether a handler can be retried is determined by the cause of the failure and whether the 
event hander is marked transactional, as shown here:  
Any 
Illegal operation: Syntax error in 
parameter 
n/a 
Failure 
Generate Event 
Illegal operation: Any attempt to 
generate a framework event 
n/a 
Failure 
Any 
Unexpected error 
No 
Failure 
Yes 
Success 
Cause of 
Failure 
Event 
transactional 
Handler 
transactional 
Retryable 
Retry point 
Event 
Variables 
Illegal 
operation 
n/a 
n/a 
No 
n/a 
n/a 
Any legal 
operation 
Yes 
n/a 
No 
n/a 
n/a 
Any legal 
operation 
No 
Yes 
Yes 
InitialAction 
Re-initialized 
Unconditional 
Fail Event 
action 
No 
No 
Yes 
InitialAction 
Re-initialized 
Conditional 
Fail Event 
action 
No 
No 
Yes 
CurrentAction 
Maintained 
Unexpected 
error 
No 
No 
Yes 
CurrentAction 
Maintained 
Action type for 
the current 
event action 
Condition 
Ignore Failure 
option selected? 
Result 
(Event 
Status)

When retrying a single handler, whether the handler runs synchronously or asynchronously depends 
on the parameter passed to the API, not the handler’s definition. When retrying an event, the handlers 
are run as shown in this table:  
An event can have a synchronous handler that is not retryable, but it still retries any asynchronous 
handlers that can be retried. In this case, any synchronous handlers that would have come after the 
failed handler will not be run. 
The Event or EventHandler Result must be cleared when retrying the handler. However, the previous 
handler result is saved in a handler variable called PreviousResult, and the event results are saved in 
an event parameter also called PreviousResult. 
Transactions 
By definition, a transactional event is an event or set of event handlers in which all must complete 
successfully before any data is committed in the system. If any handler fails, then the system rolls 
back (reverts) all data to its initial state. 
If the transactional event contains any adjourning event actions, the system modifies this behavior 
somewhat: Any actions taken up to the first adjournment, between each resumption of an 
adjournment and the beginning of the next adjournment, and after the last resumption, are each 
committed separately. 
The system treats any asynchronous event handlers as if they belong to an asynchronously 
generated non-transactional event. In other words, because they are outside the synchronous flow, 
these event handlers are not treated as part of the transaction. 
For the specifications of synchronously and asynchronously generated events, see the table for 
“Summary of synchronous functionality” on page 121. 
Transactions with synchronous events 
An event generated synchronously without the Transactional check box selected (on the Event 
Handlers form) either: 
z
Runs in the current transaction state of the firing thread (if no lower-level transactioning is 
specified). 
z
Handles transactions at the event handler or event action level, as explained in these points: 
z
In the database tier, this occurs naturally with no special syntax. 
Failed Synch Handler 
Failed Asynch Handler 
Restarted synchronously 
Synchronous 
Asynchronous 
Restarted asynchronously 
Asynchronous 
Asynchronous

When FireEventSp is called within a SQL transaction, any changes to the non-event system 
portions of the database (using Audit, Call Database Method, and Run Background Task 
event actions) become a part of that transaction, which can be rolled back after FireEventSp 
returns. 
When FireEventSp is called outside a SQL transaction, each event action that might change 
non-event system portions of the database is wrapped in its own transaction, which is rolled 
back in case of failure, except when the containing event handler is marked Transactional. 
Changes to event system state data are performed on a separate connection, so they survive 
any rollback of the encompassing or wrapping transactions. 
z
In the middle tier, any execution methods for database-related event actions must enlist in an 
existing transaction or create a new one. 
To include the entire event in a single transaction, call the FireApplicationEvent method from a 
hand-coded IDO method that is marked Transactional in the IDO metadata. In this case, the 
execution methods for the database-related event action enlist in the transaction created by 
the IDO Runtime for that transactional IDO method. 
When the FireApplicationEvent method is called from a hand-coded IDO method that is not 
marked Transactional and whose caller is not in a transaction state, each event action 
execution method creates a new transaction, which is rolled back in case of failure, except 
when the containing event handler is marked Transactional. Changes to event system state 
data are performed in a separate connection (except in suspend-validating mode), so they 
survive any rollback of the encompassing or wrapping transactions. 
z
The client is not permitted to control transactions that span form event handler calls. Client-
tier event-firing requests are passed directly on to the MGCore.Events.FireEvent IDO method. 
A failure of a synchronous event returns an error condition to the firing thread. For framework (Core) 
events, this causes the entire current transaction to be rolled back. For application events, whatever 
generated the event (stored procedure/trigger, .NET method, or VB.NET script) is responsible for 
trapping the error condition, accomplishing a rollback of the current transaction, and throwing 
execution to an appropriate recovery point in or out of that code. 
Event handlers marked Transactional 
An event handler marked Transactional is wrapped in: 
z
A new SQL transaction when executed in the database tier. 
z
A new transaction when executed from the middle tier, if no encompassing transaction is active at 
the trigger point of the outermost enclosing event. 
This event handler cannot contain any adjourning event action types (for example, Prompt, Wait, or 
Sleep), but it can be marked Asynchronous itself. If this event handler ends in a failure, the wrapping 
transaction is rolled back (assuming it was created).

Event handler not marked Transactional 
An event generated asynchronously without the Transactional setting does not run in a transaction 
state. Event handlers that are not marked Transactional, for a synchronous event generated from a 
middle-tier non-transactional custom IDO method, are handled this way: 
z
An event can be generated asynchronously with a Transactional setting that indicates that a new 
transaction is begun and the entire database-related effects of its synchronous event handlers are 
committed if they all succeed or rolled back if any fail. 
z
Any asynchronous event handlers are treated as if they belong to an asynchronously generated 
non-transactional event. 
Rolling back transactions 
These conditions cause the system to set the Transactional setting on a new event state row: 
z
FireEventSp or FireApplicationEvent() detects an enclosing transaction. 
z
FireEventSp, FireApplicationEvent(), PostEventSp, or PostEvent() receives a Transactional 
setting. 
This event state setting signals the system administrator that when this event state is finished and not 
rolled back, everything happened that was expected to happen. 
In a synchronous multi-event situation, to encode the proper information in the Rolled Back setting, 
an enclosing transaction that contains one or more FireEventSp or FireApplicationEvent() calls must: 

Once, before calling FireEventSp or FireApplicationEvent(), call EventBeginTransactionSp or 
EventBeginTransaction(). 
This uses a separate transaction to clear a storage area to record the row pointers of the event 
state rows to be created and returns a transaction identifier to be passed to FireEventSp or 
FireApplicationEvent(). 

Pass that transaction identifier to FireEventSp or FireApplicationEvent(). 
This, in a separate transaction, records the row pointer of the new event state row. 

Upon rolling back or committing the transaction (it does not matter whether before or after), call 
EventEndTransactionSp or EventEndTransaction() and pass the transaction identifier and 
whether a commit or rollback will be/was performed. 
This uses a separate transaction to set the Rolled Back setting on the stored event state rows (if 
rolling back), and clears the storage area. 
If this is neglected, the system administrator cannot determine why database actions that appear to 
have finished successfully, according to the status forms, are not reflected in the database. 
In asynchronous sitations, and when a failure is detected by the event system, the Rolled Back 
setting for the failing transactional event is set by the event system.

The Framework Event Service 
The Framework Event Service is an independent process that can run on any utility server. Each 
instance of the Framework Event Service monitors the event queue for any number of configurations 
defined locally. 
For load-balancing purposes, this service safely acquires work from the database queue of each 
configuration's application, so that multiple event services can run on one or multiple servers. The 
event service monitors the event queue for these events and handlers: 
z
New events that have been queued by means of asynchronous generation methods or 
suspending framework events, as found in the Queued Event table 
z
New event handlers that have been queued by means of the firing of asynchronous event 
handlers, as found in the Queued Event Handler table 
z
Resuming event handlers that had been adjourned, and have now completed a Prompt, Wait, or 
Sleep event action, as found in the Event Handler Status table having a value in Retest At Date 
that is older than the current date and time 
z
Resuming event handlers that had been adjourned, and have now completed a Discover File 
action, as found in the Event Handler Status table having a value in Path To Watch and no value 
in Last Watched Date 
z
Running event handlers whose current action has timed out, as found in the Event Handler Status 
table having a value in Times Out At Date that is older than the current date and time 
z
Active event triggers 
z
Continuing events that have successfully retried a previously failed handler, as found in the Event 
Status table having a value in Continue After Handler Row Pointer 
Setting up the Framework Event Service 
To set up the Framework Event Service to monitor specified configurations, you must specify each 
configuration individually on the Event Service tab of the Service Configuration Manager utility. 
Note: If you do not do this setup, any event handler you create that requires the event service will not 
work until you do. 
For more information, including the procedure, see the online help for the Service Configuration 
Manager utility. 
If you want to use the IDO Runtime Development Server (IDORuntimeHost.exe) for development 
work, you must also temporarily remove the dependency that the Event Service has on the IDO 
Runtime service. For more information, including the procedure to do this, see the online help for 
WinStudio developers. 
Processing order in the Framework Event Service 
The Framework Event Service processes any queued events in "first in, first out" (FIFO) order.

Because the event service could receive a request to run something while it is executing a prior 
request, all requests are queued for execution in the order requested. If the new request happens to 
be the only one in the queue and the event service is not busy, the request is executed at the next 
polling. 
When the event queue is empty, and immediately after processing each queued event or event 
handler, the event service checks the Event Handler State and Event Trigger tables for any items 
whose Retest At time setting has arrived or passed. 
The event service then checks the Event Handler State table for any items for which the timeout has 
expired, that is, the Times Out At time setting has arrived or passed. The event service processes 
these in order (that is, oldest first), using the Retest At time or Times Out At time to determine the 
order. 
After this, the event service checks the event queue again for any incoming items. 
Administrative details 
To eliminate the possibility of deadlocks when manipulating event data, a second database 
connection is used for event data modifications, that is, separate from the one used by the event 
action execution methods. Also, any event data modifications that do not need to be available to other 
processes—that is, any tier of any interactive user session or other event service instances—are 
made in memory and written only when required. 
To avoid overtaxing the utility server, the Framework Event Service administrator has control over the 
minimum interval for these attributes: 
z
RetestInterval parameter on Wait event actions 
z
Interval parameter on Sleep event actions 
z
RetestInterval attributes on event triggers 
When any of these attributes is referenced, if the designer-specified value is greater than zero but 
lower than the minimum interval for the Framework Event Service, the minimum value is used. 
The Framework Event Service logs various levels of messages to the Infor framework Log Monitor. 
Events and event handler revisions 
The system creates a set of event handler revisions the first time: 
z
The event is generated or any of its handlers executes. 
z
The event is generated after any of its constituent handlers or their actions has been modified in 
any way. 
z
Any of the event’s handlers executes after any of its constituent actions has been modified in any 
way.

Modifications can include additions, changes, or deletions to the handlers or actions associated with 
the event or handler. 
When the revision is created, the system copies all of the event's handlers and actions to a read-only 
table. The event or handler then uses the data in this read-only table when executing the handlers 
and actions, until a new revision is created. 
Revisions are used to help ensure that the metadata used by an event and its handlers and actions is 
not altered while the event is executing. In some cases, it can take the system a period of time to 
finish executing an event's handlers, either because of the processing time involved, or because the 
system is waiting for some input or response before it can continue. It is possible that someone could 
make changes to the event's handlers and actions while the event is processing or waiting, and that 
these changes could affect the execution of the event that is in progress. 
Revisions were developed to address this kind of potential problem. When an event fires, the event 
and its handlers use the revisions that are in effect at the time they start executing until they are 
finished. 
Example 
Suppose you are using an event to send notices to a manager when a customer order is more than 
$10,000. The manager must approve the order before it can be processed. 
During a transfer of responsibilities from one manager to another, a new manager is assigned the 
responsibility of approving such orders. The system administrator makes the change of notice to the 
appropriate event action. 
However, the original manager still has a few orders pending approval. These orders continue to use 
the metadata for the revision in effect at the time they were created, awaiting that manager's 
approval. In the meantime, the new manager receives notices for any subsequent orders, because 
the first new order generates a new revision using the information for the new manager.

### Chapter 3: Designing and Using Events
*Pages 31-52*

Chapter 3: Designing and Using Events 
and Handlers 
Infor has built in to the system a number of events and handlers that are available for immediate use. 
In addition, if you have an add-on product distributed by one of Infor’s business partners, they might 
also have added their own events and handlers that you can use. 
You can also design and create your own custom events and handlers to automate tasks for your 
particular needs. This chapter provides information about the key elements of the Application Event 
System and the procedures for creating and using custom events and handlers. 
Note: If you are creating and using your own custom events and handlers, we recommend that you 
refresh the metadata cache periodically. This should be done after doing development work, before 
testing, and after synchronizing your metadata on your system. See “Refreshing the metadata cache” 
on page 50. 

applicable, procedures for creating and using various elements are also provided. 
About the Access As identifier 

is used to: 
z
Indicate who (what organization) created and "owns" an event or related event system object. 
z
Prevent unauthorized developers from modifying or deleting event system objects that they do 
not own. 
The Access As identifier is also used to indicate ownership and modification rights for certain IDO 
metadata. It might also be used in the future for other, similar metadata. 
Generally, the Access As identifier falls into one of three classifications:

z
Core – Indicates that the object is one that Infor created and owns. These event system objects 
are used for the framework forms and operations. 
z
Any other name – Indicates that the object was created by and belongs to an application created 
either by Infor or by one of Infor’s business partners or other authorized vendors. 
z
Blank – Indicates that the object was created by and belongs to the end customer. 
Within WinStudio, several forms include an Access As field. On the Access As form, this field 
indicates the current Access As value. This is the value assigned to any new event system objects 
you might create. On all other forms, this field indicates who has ownership of the pertinent object 
metadata, in other words, who created and owns it. 
You can only modify or delete metadata for event system objects that have the same value as on the 
Access As form, in other words, application event system objects that your organization has created 
and owns. 
Note: If you need to change the Access As identifier, see the online help for the procedure. 
With a few exceptions (noted where applicable), you can attach your own event triggers and handlers 
to event system objects owned by other organizations (that is, with a different Access As identifier 
than yours), but you cannot directly modify or delete those event system objects. 
About events 
An event is defined as a uniquely named situation that can be triggered by: 
z
An action performed by somebody working in the system. 
z
A particular condition that occurs while the system is running. 
z
A certain value that is exceeded in a database record. 
z
Another event’s handler. 
z
Other, similar occurrences. 
Event types 
Events can be one of three general types: 
z
Core, or framework, events – These are events that Infor has defined and built in to the system. 
They are tagged with an Access As identifier of Core. 
These events generally fall into one of two categories: 
z
IDO (business process-related) events that are generated when certain IDOs are invoked. 
These IDOs include IdoOnItemInsert, IdoOnLoadCollection, IdoOnInvoke, and others. You 
can identify these events easily by their names, which begin with the letters Ido. 
z
Session events that are generated when certain session activities take place. 
These include SessionOnLogin, SessionOnLogout, and SessionOnVarChanged. 
These events are always synchronous and transactional. Some can be optionally suspended to 
await user responses.

z
Application-specific events – These are events that typically have been created by Infor, its 
business partners, and authorized vendors. They are tagged with an Access As identifier that 
indicates what application or development organization they belong to. 
z
Customer-defined events – These are events that a developer in an end-customer organization 
has created. They are tagged with a blank Access As identifier, which indicates that they were 
created by and belong to the customer. 
See “About the Access As identifier” on page 31. 
Defining events 
Events can be defined (named) on these forms: 
z
Events 
z
Event Triggers 
z
Event Handlers 
To define an event, specify the name of the event in the Event Name field of one of these forms.
Note: If you do not name the event on the Events form, it is still available to the drop-down lists on 
other forms. Events named on those forms, however, do not display on the Events form. So, if you 
want the event to display on the Events form, you should name the event on that form. 
When an event is defined, or named, it is really just that: a name. Until you define a way for it to be 
triggered or initiated, the event remains just a name. This can be done using either the Event 
Triggers form, the Event Handlers form, or both. 
See “About event triggers” on page 34. 
For more information about any of these forms, see the online help for that form. 
Modifying events 
Once an event has been created and saved, the only thing you can modify is the event's description. 
The event name and other attributes are locked. 
Note: You can modify an event's description only if the Access As field has the value of the current 
Access As value, as displayed on the Access As form. 
To modify an event's description: 

Open the Events form and select the event you want to modify. 

In the Description field, modify the description text as desired. 

Save. 
Deleting events 
If you are certain you no longer need an event and you want to delete it, you can.

You can delete an event only if the Access As field has the value of the current Access As value, as 
displayed on the Access As form. 
To delete an event: 

Open the Events form and select the event you want to delete. 

From the Actions menu, select Delete. 

Save. 
About event triggers 
An event trigger is defined as a condition that causes a particular event to fire, more-or-less 
independent of anything that might be happening in the user interface. The event trigger carries a set 
of event trigger parameters for use when the event fires. 
An event trigger can be set to fire the event only once, or it can be set to retest for its condition after 
waiting a certain amount of time since either of these situations was true: 
z
The trigger last successfully fired the event. 
z
The trigger last tested unsuccessfully for its condition. 
In both cases, you can set the interval for the event trigger to wait, both for the successful firing of the 
trigger and for the unsuccessful test for the trigger conditions (using separate settings). Testing and 
retesting is accomplished by means of polling; this is not a true interruptive trigger. 
An event trigger carries with it the user name and configuration in effect at the time it was defined. 
This data is passed on to the event state when the trigger fires the event. 
Defining event triggers 
Event triggers are defined using the Event Triggers form. Use this form to determine the condition 
that will fire the event, set the parameters to be passed to the event when it fires, and specify retest 
intervals. 
To create an event trigger: 

Open the Event Triggers form. 

Press F3. 

From the Actions menu, select New. 

From the Event Name drop-down list, select the event for which you want to define a trigger. 
Note: You cannot define a trigger for a framework (Core) event. 

On the Trigger tab, in the Condition field, specify the condition at which the event is to fire. 
See “Triggers and conditions” on page 35.

On the Parameters tab, specify the name and values for any event parameters for which you 
need to pass values to the event handlers when the event fires. 

Set other options on this form as desired. 
For information on other form options, see the online help for each field. 

Save the form. 
Triggers and conditions 
Each event trigger must contain a condition consisting of one of these: 
z
A Boolean expression 
z
Two non-Boolean expressions separated by a comparison operator 
Examples 
z
This example causes the event to fire when seven days have elapsed since the current result of 
the database function dbo.LastEntryDate(): 
DATEDIFF(day, DBFUNCTION("LastEntryDate"), CURDATETIME()) > 7 
z
This example causes the event to fire when the balance on a certain customer's order is greater 
than $10,000: 
DBFUNCTION("OrderBalance", GC(BigCustNum)) > 10000 
z
This example causes the event to fire on the first day of each month: 
DATEPART(day, CURDATETIME()) = 1 
Note: The condition should generally involve a time operation, a database calculation, or both. This is 
because time and the database are the only known factors that can undergo change from external 
stimuli (that is, by the forward movement of time or by the actions of other application users, 
respectively). 
Retesting triggers 
When the event trigger's Retest At Date setting becomes older than the current system clock time, 
the event trigger is available to be processed by the event service. This happens when the event 
service is free from processing any waiting queued events and handlers and any already-waiting 
triggers that need to be tested or retested. 
To process the event trigger, the system parses the condition, evaluates it, and, if the condition 
evaluates to TRUE, then the event fires. At that point, the Retest At Date setting is set to the current 
time plus the amount of time set for the Trigger Reset Interval. If the Trigger Reset Interval is set to 
0 (zero), then the Active inidicator is cleared, which indicates that the trigger is not to be retested. 
If the condition evaluates to FALSE, then the Retest At Date setting is set to the current time plus the 
amount of time set for the Condition Retest Interval. If the Condition Retest Interval is set to 0 
(zero), then the Active indicator is cleared, which indicates that the trigger is not to be retested.

About event handlers 
An event handler defines the actions to be taken upon the firing of a particular event. Each event 
handler is comprised of one or more event actions and, optionally, an initial state. 
Each event can have multiple event handlers that execute when the event fires. In such cases, the 
handler sequence number and other factors determine the order in which event handlers are actually 
processed. 
For more information about event actions, see “About event actions” on page 37. 
For more information about initial states, see “About event variables and initial states” on page 41. 
Defining event handlers 
Each event handler is uniquely defined in the system by the combination of an event name and a 
handler sequence number. Both of these are set on the Event Handlers form. Event handlers also 
must have one or more associated event actions. 
See “About event actions” on page 37. 
To create an event handler: 

Open the Event Handlers form. 

Press F3. 

From the Actions menu, select New. 

In the Event Name field: 
z
Select the event for which you want to create a handler. 
This sets up the event handler for an already-defined event. 
z
Specify the name for an event which has not been previously defined. 
This effectively defines a new event as well. 

(Optional) To control the order in which the event handler executes (especially with respect to 
existing event handlers), use the Keep With and Chronology fields, or the Event Handler 
Sequence form. 
See “About event handling and order” on page 47. 

Save the new event handler. 

Use the Event Actions button to open the Event Actions form and create the actions to be 
performed when this event handler is executed. 
See “About event actions” on page 37. 

After closing the Event Actions form, set the other options on the Event Handlers form as 
desired. 
An event handler can be restricted to execute only in relation to a specific set of conditions. For 
example, a particular event handler might be defined to execute only when the associated event 
is triggered by an action on a particular form or when a particular IDO is involved.

An event handler can also be set to execute synchronously or asynchronously, or as part of a 
transactional event or set of event handlers. 
See “Synchronicity” on page 16 or “Transactions” on page 24. 
For information about the other options, see the online help for each option. 

Save the event handler. 
About event actions 
An event action is defined as a unit of work to be performed during the execution of an event handler. 
A single event handler can have multiple event actions, but each action is assigned to a single event 
handler. 
Depending on its action type, an event action can do such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event handler. 
z
Set event variables. 
z
Call methods or web services. 
z
Perform other predefined tasks. 
Defining event actions 
To define new event actions, open the Event Actions form using the Event Actions button on the 
Event Handlers form. If you open the Event Actions form from the Explorer or the Select Form 
dialog box, you can only view and modify existing actions. 
To create an event action: 

Open the Event Handlers form. 

Create a new event handler; or, in the grid view, select the event handler for which you want to 
create the action. 

Click the Event Actions button. 

(If there are no existing event actions) From the Actions menu, select New. 

In the Action Sequence field, specify a number. 
This number determines the order in which actions for a particular handler are processed. 

In the Event Actions form, Action Type field, specify the type of action to be performed. 
Note: If you are creating a new handler, you must save it before you can do the next 
step.

For a complete list of action types and what they do, see “Event action types” on page 126. 

To define the parameters for the action, click Edit Parameters and use the associated event 
actions parameter form. 
For more information about defining parameters, see “About event action parameters” on 
page 38. 

To verify that the syntax is correct, click Check Syntax. 
If you have any syntax errors, fix them before proceeding. 

If the action involves a variable to be used in event messages and you want to restrict the 
variable's accessibility on the target form, set those restrictions on the Variable Access tab. 
For more information about setting variable access, see the online help for the Variable Access 
tab. 
10 Save your changes and close the form. 
About event action parameters 
Depending on the action type, you also specify optional parameters for each event action type. You 
can specify parameters in any order for a particular action. To list multiple parameters, specify them 
one after another, specifying either a space or nothing between them. Event action parameters are 
defined on the Parameters tab of the Event Actions form. 
TIP: You can use the event action parameter forms to define the parameters. When you do, the 
parameters are returned to the Event Actions form properly formatted and free of syntax errors. 
See “About event action parameter forms” on page 40. 
The syntax for each event action parameter is as follows: 
FUNCTION(value)
TIP: Although it is not a requirement that function names be specified using all uppercase letters, we 
recommend the practice, as it leads to greater ease of recognition and readability. 
The value enclosed in parentheses can consist of: 
z
A constant number 
z
A literal string enclosed in quotation marks 
z
A Boolean value: TRUE or FALSE 
z
An event function call 
These can be nested. For more information, see “Nesting function calls” on page 39. 
z
An expression consisting of a number of these elements combined using operators. 
You can also use the parentheses following the function to wrap expressions that signify operations to 
be performed on the results of the expression. 
For example, the function V takes as a parameter the name of a variable. This function can be 
placed in the parameters for other functions, as in this example:

METHOD(V(FuncNameVar)) 
For more information about event action parameters, including a list of all acceptable parameters, 
their meanings, and examples, see “Event action parameters” on page 126. 
For the complete expression grammar for constructing event action parameters, see Appendix C, 
Expression Grammar. 
Function types 
Functions can be any of three basic types: 
z
Parameter functions — These are functions whose parentheses wrap a "parameter" to the event 
action. For example, these are all typical parameter functions: 
z
SETVARVALUES 
z
METHOD 
z
INTERVAL 
z
EVENTNAME 
These functions must always appear at the "root" level and can never be nested inside any other 
type of function. 
These functions are identified in this documentation generically as PARAMS(…). 
z
Value functions — These are functions that call event values such as: 
z
SUBSTITUTE 
z
DATE 
z
ABS 
z
CEILING 
These types of functions can never appear at the "root" level but must be nested within another 
function construct (either a parameter or another function). 
These functions are identified in this documentation generically as FUNCTION(…). 
z
Word functions — These are verbatim words used inside certain event function calls, such as: 
z
AS 
z
STRING 
z
NUMBER 
z
DAY 
z
DATE 
Note that some of these can also be used as event function calls. These functions always appear 
within an event function call, however. 
These functions are identified in this documentation generically as …WORD… 
Nesting function calls 
When defining event action parameters, keep these rules (as specified in the previous section) in 
mind:

z
PARAMS(…)-type functions can never be nested. 
z
FUNCTION(…)-type functions must be nested and can be nested either within PARAMS(…) 
functions or within other FUNCTION(…) functions. 
z
…WORD…-type functions must be nested within FUNCTION(…)-type functions. 
This is an example of an event action parameter that uses nested functions: 
PARAMS(…FUNCTION1(…FUNCTION2(…WORD1…)…WORD2…)…) 
Passing parameters from actions 
Parameter lists to methods, scripts, web services, and generated events are always enclosed in a 
PARAMS(…) function and delimited by commas. Each parameter is specified in one of these ways:  
Setting variable and parameter values 
You can set values for event variables and parameters using these syntaxes:  
About event action parameter forms 
To make it easier to create event action parameters that are properly defined and formatted, each 
event action type has a corresponding event action parameter form. These forms allow you to build 
appropriate sets of parameters for each action type by providing options that pertain to that action 
type. 
Syntax 
Direction 
Meaning 
V(var) 
Input 
Pass in the value of the variable var. 
expression 
Input 
Pass in the value obtained by evaluating the 
expression. 
RV(var) 
Input and output 
Pass in the value of the variable var, and 
place the output value into the same variable. 
Event action type 
Type of storage 
Syntax 
Call Database Method 
Call IDO Method 
Variable 
PARMS(RV(var)) 
Parameter 
PARMS(RE(param)) 
Generate Event 
Load IDO Row 
Variable 
SET(RV(var)=name) 
Parameter 
SET(RE(param)=name) 
Set Values 
Variable 
SETVARVALUES(var=expr) 
Parameter 
SETPARMVALUES(param=expr)

For example, if you are creating an event action of the type Notify, when you open the associated 
event action parameter form, you see something like this:  
Notice that each editable text field is labeled with a button on the left. This is a fairly typical pattern for 
event action parameter forms. With each button/field pair, you have the option to either specify the 
value for that parameter in the field or click the button. Clicking the button opens another form that 
pertains to the parameter associated with that button and that allows you to build just that parameter. 
Some options are presented using combo boxes that also have drop-down lists from which you can 
select appropriate values for that field. Some options are not accompanied by buttons at all. Other 
options are selected (or not) using check boxes, as with the Save in Sent Items in this example. 
Very few options on any given form are considered required. As a rule, only those fields that you 
populate return parameter values to the Event Actions form. Where strings require quotation marks, 
the system inserts them automatically. Where expressions are nested inside other expressions or 
parameter statements, the system automatically places parentheses where they are required. 
The result is that, by using the event action parameter forms, you can eliminate most—or more likely 
all—syntax errors in your parameter statements. 
About event variables and initial states 
If an event handler has variables associated with it, those variables can be assigned an initial state, 
that is, a set of values they are assigned when the event handler starts to execute. Each initial state 
consists of: 
z
A name that identifies it in the system 
z
Any number of event variables with the initial values they are to have when the event handler 
starts to execute

For example, you might want to use with your event handlers variables with these initial values:  
Initial states are defined using the Event Variable Groups form. Once created, you can use a defined 
initial state with any other event handler by selecting it in the Initial State field on the Event Handlers 
form. 
About event global constants 
An event global constant is defined as a named static value that event expressions can reference 
during processing of the associated event handlers. 
Example 
For example, you could use a global constant to create a list of managers who are authorized to 
control customer credit limits. You could then reference this global constant whenever you create an 
event handler that sends a notification (Notify event action) regarding a customer’s credit limit. This 
practice allows you to use the list for multiple event handlers without having to hard-code the list of 
names in each event handler’s actions. It also allows you to change the list in one place and have that 
one change affect every event handler that uses it. 
For more examples of how global constants can be used, see Appendix A, Sample Scenarios. 
Defining and using event global constants 
Event global constants are defined using the Event Global Constants form. 
The system references a global constant using a function mechanism that allows dynamic evaluation 
at each reference. 
Event global constants can be especially useful when defining a set of choices to offer the recipients 
of a prompt message. For example, a global constant named PromptChoicesYesNo can be defined 
with the value 1,sYes,0,sNo. You can then reference this constant for any prompt event action, using 
the expression: 
Name of variable 
Initial value 
Comments 
Increment 

— 
ItemTypes 
AB 
— 
TimesRemaining 
GC(MaxTimes) 
In this case, the value is determined by the 
value of the MaxTimes global constant.

CHOICES(GC(PromptChoicesYesNo)) 

The system includes a set of specialized forms created to enable you to create and use your own 
custom application events. With the exception of the Access As form and the System Configuration 
Parameters form in this table, these forms are located in the Explorer under Master Explorer > 
System > Event System. The Access As and System Configuration Parameters forms are 
located one level up, at Master Explorer > System. 
Access to these forms is controlled by the System Administration authorization group. 
This table lists and briefly describes the use of the event system design forms. 
Form name 
Description/Use 
Access As 
Although not directly used in the creation and customization of application 
events and handlers, this form displays the current Access As setting. 
This, in turn, is an indicator of which event system elements you are 
authorized to modify and/or delete. 
See “About the Access As identifier” on page 31. 
Events 
This form is used to name events. Once named here, events are available on 
other forms as well, particularly the Event Triggers and Event Handlers 
forms. 
See “About events” on page 32. 
Event Triggers 
This form is used to define event triggers, which set conditions that cause a 
named event to fire. 
See “About event triggers” on page 34. 
Event Handlers 
This form is used to display and define event handlers, which determine the 
work to be done when an event fires. 
See “About event handlers” on page 36. 
Event Handler 
Diagram 
This form is used to present a graphical representation of an event handler 
flow. You can also use this form to access the Event Actions form for 
selected event actions, to view or modify them. Finally, you can also add event 
actions to an event handler flow using this form. 
See the online help topic "Using the Event Handler Diagram Form." 
Event Handler 
Sequence 
This form is used to change the order of any handlers that have the current 
Access As identifier (as indicated on the Access As form). 
See the online help for this form.

Event Actions 
This form is used to display and define the actions to be performed by a 
particular event handler during its execution. These are the individual tasks 
accomplished by the event handlers. 
See “About event actions” on page 37. 
Event action 
parameter forms 
These forms are used to define the event action parameters for each action 
type. 
See “About event action parameter forms” on page 40. 
Event Variable 
Groups 
This form is used to display and define initial states, which are sets of event 
variables and the initial values they are to pass to the event handler when it 
starts to run. 
See “About event variables and initial states” on page 41. 
Event Global 
Constants 
This form is used to display and define event global constants, which are 
static values that can be accessed and used by expressions during the 
running of an event handler. 
See “About event global constants” on page 42. 
System 
Configuration 
Parameters 
This form is used to define certain parameters that affect the system 
configuration. 
Although not directly used in the creation and customization of application 
events and handlers, you can use this form to control some aspects of how 
events and handlers behave on the system. These aspects are concerned 
mostly with retest and reset intervals that globally govern when and how often 
various conditions can be retested or events can retry. 
See the online help for this form. 
Workflow Event 
Handler 
Activation 
This form is used to activate predefined event handlers that represent 
common workflows. You must specify some information, such as users or e-
mail addresses that will be notified when an event occurs. You can also copy 
and modify these event handlers. 
Note: This form is not available with all Mongoose-based applications, including 
Mongoose as a stand-alone application. 
See the online help in your application for this form. 
Form name 
Description/Use

This diagram shows the functional relationship between the design forms and elements for the 

 
Setting up custom events and handlers 
To create and use your own custom application events, there are several important steps and 
considerations to keep in mind. You must: 
z
Design and define your custom event. 
See “Designing a custom event” on page 46. 
z
Carefully plan and set up the order in which event handlers and actions execute. 
See “About event handling and order” on page 47. 
z
Periodically refresh the metadata cache, to ensure that you are working with the most current 
version of the event metadata. 
See “Refreshing the metadata cache” on page 50.

Designing a custom event 
When you create a custom event, you must also define what will fire the event. In the current 
WinStudio system, there are four ways to generate a custom event: 
z
Create an event trigger using the Event Trigger form. This is probably the easiest and most 
common way to generate a custom event. 
z
Use an action of type Generate Event in another event handler. 
z
Use a form (WinStudio) event handler with a response type of Generate Application Event. 

handlers described in this guide.) 
z
Use the WinStudio API to write a custom script that generates an event. 
These steps represent a typical process for creating custom application events: 

(Optional) If you want to name the event before defining how it should be triggered and/or 
handled, use the Events form. 
If you do not name the event on the Events form, it will still be available to the drop-down lists on 
other forms (specifically, the Event Triggers and Event Handlers forms). Events named on 
those forms, however, do not display on the Events form. So, if you want the event to display on 
the Events form, you should name the event on that form. 
See “Defining events” on page 33. 

(Required only if you want to fire the event using an event trigger) To define one or more triggers 
that will fire the event, use the Event Triggers form. 
See “About event triggers” on page 34. 

To define one or more event handlers that execute when the event fires, use the Event Handlers 
form. 
See “About event handlers” on page 36. 
Each event can have multiple handlers that execute when the event fires. The order in which 
multiple handlers execute is controlled by a number of factors. 
See “About event handling and order” on page 47. 

To define one or more event actions for each event handler, use the Event Actions form. 
See “About event actions” on page 37. 

If required, to name and define an initial state for the event handler to use, use the Event 
Variable Groups form. 
See “About event variables and initial states” on page 41. 

If required, to name and define any global constants for the event handler to use, use the Event 
Global Constants form. 
See “About event global constants” on page 42. 

Test the event and its triggers and handlers on a test system before implementing them on your 
live system.

For specific examples of how to create and use custom application events, see Appendix A, Sample 
Scenarios. 
About event handling and order 
There are two basic ways to arrange the order in which events that have multiple handlers and 
actions execute those handlers and actions. 
Ordering event handlers 
When an event handler is first defined and saved, the system automatically assigns it a handler 
sequence number. When the event handler is first saved, the system checks to see if there are 
already any other handlers associated with the named event. Depending on the results of that check, 
the system then assigns 1 to the handler (if there are no other handlers associated with the event) or 
the next available integer (if there are other handlers associated with the event). 
In general, then, if an event uses multiple event handlers, by default, the system uses the handler 
sequence numbers to determine the order in which the handlers execute. 
It is possible, however, to indirectly alter this default order. This is done either by: 
z
Using the Keep With and Chronology fields on the Event Handlers form. 
z
Moving your own adjacent event handlers up or down in the sequence, using the Event Handler 
Sequence form. 
To alter the default order in which event handlers execute using the Keep With and Chronology 
fields on the Event Handlers form: 

(Optional) From the Keep With drop-down list, select the event handler you want to use as a 
reference point and anchor for the current handler. 
This step is not required if you are using the First or Last option in the Chronology field. 

From the Chronology drop-down list, select the option you want the current handler to use with 
respect to the handler you selected in Step 1. Options include: 
z
First – Executes the current handler before any other handlers. 
z
Before – Executes the current handler just before the referenced handler. 
z
Instead – Executes the current handler in place of the referenced handler. In this case, the 
referenced (original) handler does not execute at all. 
For exceptions to this rule, see “Overriding others’ handlers” on page 177. 
z
Exclusively Instead – Executes the current handler instead of the referenced handler and 
any other handler that may be referenced to execute instead of (Instead) that same handler. 
z
After – Executes the current handler just after the referenced handler. 
z
Last – Executes the current handler after all other handlers. 
For more information about reordering event handlers, including some detailed examples, see 
Appendix E, Synchronization of Metadata.

Resequencing event handlers 
Use the Event Handler Sequence form to change the sequence in which your adjacent event 
handlers execute for a specified event. 
Note: 
z
This form is intended to be accessed as a linked form, from the Event Handlers form only, using 
the Resequence button. If you open it in standalone mode, the results can be unpredictable. 
z
You can change the order only of event handlers that have the same Access As value as 
displayed on the Access As form, and then only if they are grouped together (that is, adjacent to 
one another in the sequence), and within the group. You cannot use this form to change the 
sequence of event handlers with other Access As values. 
z
To change the order of your event handlers with respect to those of others (that is, with different 
Access As values), use the Keep With and Chronology fields on the Event Handlers form. 
To change the sequence of an event handler: 

In the grid view, select an event handler that has your Access As value. 

Click the Up or Down button to move the selected handler up or down in the sequence, keeping 
in mind the restrictions mentioned above. 
If you try to violate those restrictions, the system generates an error and you cannot complete the 
move. 

Save. 
Ordering event actions 
A single event handler can contain multiple event actions. When you define an event action, you must 
assign an action sequence number to it (in the Action Sequence field of the Event Actions form). 
You can assign any number you want in that field, and the system automatically sorts the actions in 
the correct sequence on the Event Handlers form. When the event handler executes, the system 
uses this Action Sequence number to determine the order in which the actions execute. 
The only exception to this rule is that, if you select a particular action (other than 1) in the Initial 
Action field of the Event Handlers form, then processing of the event actions begins with the 
designated action and proceeds from there. So, for example, if you have four actions associated with 
a handler, and you later decide you want action number 3 to be the starting point, you would select 3 
in the Initial Action field. In this case, only actions 3 and 4 would execute. The system would skip 
over actions 1 and 2. (You could later execute these actions by using an action type of Branch or 
Goto, with one of these actions as the destination.) 
Determining names of IDO collections and components 
To create custom event handlers and actions, you are often required to know the internal names of 
the collections (known internally as "IDO collections") and the components you want to refer to. For 
example, to set up a handler, you often need the name of the IDO collection associated with a

particular form. To include dynamic content in the subject or body of a message, you often must know 
the internal name of a column or component within that IDO table. 
But what if you do not know those names? How can you find what you need? 
Determining the name of an IDO object 
To determine the name of an IDO object for an event handler definition: 

Open the form that uses the IDO collection you require. 
For example, if you are setting up an event handler to work with customer records, you would 
open the Customers form. 

Go into Design Mode for that form. 

Verify that the Form properties sheet is showing. 
If it is not, from the View menu, select the Form Properties option. 

Select the Collections tab. 
The names of all IDO collections associated with that form are displayed in the Collections list at 
the top of the form. Usually, there is only collection, which makes it easy to figure out. If more than 
one collection is listed, you might have to take further steps to determine which is the one you 
need. 
The internal name of the IDO is that part of the IDO name that displays after the period. For 
example, the Customers form uses the SL.SLCustomers IDO. The name of the IDO collection as 
you need it to create an event handler, is SLCustomers. 
Determining the name of a form component 
To determine the name of a form component: 

Open the form that has the field or other component that displays the data to which you want to 
refer. 
For example, to create a subject line that includes a customer’s ID number and name, you would 
open the Customers form. 

Go into Design Mode for that form. 

Select the desired component, for example, the Customer ID field. 

Verify that the Component properties sheet is showing. 
If it is not, from the View menu, select the Component Properties option. 

On the Component properties sheet, locate the Data Source section, Binding field. 
The component’s internal name displays in that field, after the period. For example, for the 
customer ID number, the Binding field displays object.CustNum. Thus, the Customer ID field 
name is CustNum.

Refreshing the metadata cache 
Because certain summary event metadata is cached in memory for faster performance, the IDO 
metadata cache should be refreshed periodically, after changes to event metadata (that is, after 
making changes to events, handlers, actions, triggers, and global constants). This should be done, at 
a minimum, after doing development work, before testing, and after synchronizing the metadata on 
your system. 
Note: 
z
If you have multiple utility servers in your system, you must refresh cached metadata for each 
utility server on which metadata might have been cached. The best way to do this is to use the 
second option described below. 
z
Any event metadata that is not referenced within two minutes is automatically refreshed from the 
cache. That is why you might notice that things work the way you expect, even without manually 
discarding the cached metadata. We still recommend that, as a precaution, you manually refresh 
the cached metadata to be sure. 
There are four ways you can refresh the cached metadata: 
z
By using the Discard Cache button on the Utilities tab of the Configuration Manager. For more 
information, see the Configuration Manager online help. 
z
By unloading global objects from your system (this requires that certain settings be made; see 
“Refreshing cached metadata by unloading global objects” on page 50). 
z
Be restarting the IDO Runtime Service on the application server (see “Refreshing cached 
metadata by restarting the IDO Runtime Service” on page 50). 
z
In the IDO Runtime Development Server (this requires that you be running a copy of this software 
locally; see “Refreshing cached metadata in the IDO Runtime Development Server” on page 51). 
Refreshing cached metadata by unloading global objects 
With the correct system settings, you can have the system refresh the cached metadata automatically 
every time you unload all global objects. 
To refresh cached metadata by unloading global objects: 

In WinStudio, from the View menu, select User Preferences. 

Select the Runtime Behaviors tab. 

Select the check box labeled Unload IDO Metadata With Forms. 
While working on event metadata, periodically unload global objects, and the cached metadata is 
automatically discarded and refreshed with the global objects. 
Refreshing cached metadata by restarting the IDO Runtime Service 
If you do not want to use the first option and you are not using the IDO Runtime Development Server 
on your local machine, you can discard the cached metadata by manually stopping and restarting the

IDO Runtime Service on the application server. This works because the metadata cache is not saved 
when the service is stopped. 
To refresh cached metadata by restarting the IDO Runtime Service: 

On the application server, open Control Panel. 

Select Administrative Tools > Services. 

From the list double click Infor Framework IDO Runtime Service. 

In the Infor Framework IDO Runtime Services Properties dialog box, click Stop. 

When the IDO Runtime Services Properties dialog box indicates that the service has stopped, 
click Start. 
Refreshing cached metadata in the IDO Runtime Development Server 
If you are using a local installation of the IDO Runtime Development Server, you can refresh the 
cached metadata manually. 
To manually refresh cached metadata in the IDO Runtime Development Server: 

In the IDO Runtime Development Server, select the configuration for which you want to refresh 
the cached IDO and event metadata. 

From the Configuration menu, select Discard IDO Metadata Cache.

### Chapter 4: Tracking Event System Status
*Pages 53-56*

Chapter 4: Tracking Event System Status
Some application events can take a considerable amount of time to process, especially if they involve 
event messages that require responses from the recipients. The system provides a number of tools 
and forms that allow you to track the status of application events as they execute and after they have 
finished executing. Some of these forms also allow you to temporarily adjust the behavior of handler 
execution. 
These forms are located in the Explorer under Master Explorer > System > Event System. 
Initially, these forms can be accessed only by members of the System Administration authorization 
group. 
These forms can all be used to track various aspects of event system status: 
z
Event Status form 
z
Event Handler Status form 
z
Event Queue form 
z
Event Revisions form 
z
Event Handler Revisions form 
z
Suspended Updates form 
Event Status form 
Use the Event Status form to view: 
z
The status of events that are currently running 
z
The history of events that have finished running 
This form has five tabs: 
z
Event tab – Provides options to filter for events and handlers in various states and make it easier 
to locate specific ones. 
For example, suppose you want to find data about all events that are currently suspended. With 
Filter-in-Place, you would select the Suspended check box and then execute Filter-in-Place. 
z
Handlers tab – Shows data about handlers that are currently processing or have finished 
processing.

z
Parameters tab – Shows data about the parameters associated with an event that is currently 
running. These include input parameters passed into the event, as well as output parameters 
created by handlers’ actions. 
z
Output Parameters tab – Shows data about the output parameters of an event that has finished 
running. 
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Handler Status form 
Use the Event Handler Status form to view: 
z
The status of event handlers that are currently running 
z
The history of event handlers that have finished running 
This form has four tabs: 
z
Handler tab – Shows data about the event handler itself. 
z
Actions tab – Shows only data about actions of the handler that have started. 
z
Variables tab – Shows information about variables associated with the event handler.
z
Voting tab – Shows data about the voting status of a Prompt action. 
For more information about this form and its options, see the online help. 
Event Queue form 
The Event Queue form displays a list of all asynchronous events and event handlers that the system 
has queued for processing. All information on this form is display-only. (For more information about 
synchronous and asynchronous events and handlers, see “Synchronicity” on page 16.) 
Events on the queue are processed in FIFO (first in, first out) order. The ID number on this form 
indicates the order in which events are queued for processing. 
This form also displays other information about events and event handlers that have been queued for 
processing. Each event or event handler that has been queued is displayed as a separate record in 
the grid view. 
For more information about this form and its options, see the online help.

Event Revisions form 
The Event Revisions form displays information about the event revisions associated with events. 
For more information about event revisions and how they work, see “Events and event handler 
revisions” on page 28. 
Event Handler Revisions form 
The Event Handler Revisions form shows information about event handler revisions associated with 
event handlers. All information on this form is display-only. The reason for this is that some running or 
finished handlers are using the metadata in this revision to complete their processing. To change the 
data for this event handler, you must use the Event Handlers form. 
For more information about event handler revisions and how they work, see “Events and event 
handler revisions” on page 28. 
Suspended Updates form 
The Suspended Updates form displays a list of all the update actions that are currently in a 
suspended state. This form also allows you to take selected updates out of suspension manually. 
For more information about this form, see the online help for the form.

### Chapter 5: Event Messages
*Pages 57-66*

Chapter 5: Event Messages

z
The system, as part of an event handler’s actions 
Only Notify and Prompt action types can generate messages. 
z
Other users on the system, much like e-mail 
Each message is visible only by the recipients and, optionally, the sender of that message. 
Event message-related forms 
Event message-related forms are used to view, sort, file, respond to, and send messages generated 

> Messages folder. 

z
The Inbox form 
z
The Saved Messages form 
z
The Send Message form 
The Inbox form 
The Inbox form can be accessed in a number of different ways: 
z
From the View menu, by selecting the Inbox Form option. 
z
In the Windows taskbar (notifications area), by double clicking the Inbox notification icon ( 
 ). 
z
In the same ways that any other forms are accessed. 
The Inbox form displays system messages that can come from two possible sources: 
z
Application events that employ a Notify or Prompt action type. 
z
Communications initiated and sent by individual system users to other users on the system.

This form displays only those messages which are still in the recipient’s Inbox "folder" and not 
messages that have been moved to other folders. To view those messages, recipients must use the 
Saved Messages form. The Inbox form also does not allow recipients to move messages to other 
"folders." To do that, recipients must use the Saved Messages form. 
See “The Saved Messages form” on page 59. 
When a message is received, if the recipient has set options to be notified, the system alerts the 
recipient with the selected notifications. 
See the topic "Notifications Settings" in the online help. 
Recipients can mark messages as read and, depending on how and why the message was sent, 
make other responses. 
Responding to system-generated messages 
If the message is the result of a system-generated prompt, each recipient can respond to the prompt, 
usually by means of a set of voting buttons. 
See “Prompts and responses” on page 61. 
If the message was also sent to the recipient’s external e-mail inbox, and the recipient responded to 
the e-mail message, the message in the refreshed Inbox is marked as expired and the buttons are 
inactive, so the recipient cannot respond twice. 
If the message is system-generated and involves variables, for each variable, depending on the 
Variable Access setting for the event variable (on the Event Actions form) or initial state (on the 
Event Variable Groups form) or payload status (on the Event Action Notify or Event Action 
Prompt form), recipients might be able to: 
z
Provide an optional response 
z
Provide a mandatory response 
z
Only read the variable value 
z
Not see the variable value at all 
Setting variable access 
The effective visibility and writability of each variable displayed on the Inbox form is determined by 
two things: 
z
What type of action generated the message (Notify or Prompt) 
z
The (optional) variable access level as specified on the Event Action form for the action itself 
and/or on the Event Variable Groups form for the event handler’s initial state and/or on the 
Event Action Notify or Event Action Prompt form for the action with regard to the payload 
status of the property that corresponds to the variable, when the handler is associated with an 
IDO event.

For Notify type messages 
The default for variable access is Read-Only. You can use the variable access options to override this 
to Hidden for each variable. 
For Prompt type messages 
The default for variable access is Writable. You can use the variable access options to override this 
to Hidden, Read-Only, or Mandatory for each variable. 
To change the value of a variable that might appear with a message in the Inbox form, you can do 
any of these actions: 
z
Specify the data using the Variables tab on the Inbox form as part of a response to a Prompt 
action. 
z
Use a Set Values event action with the function syntax: SETVARVALUES(PropertyName=name) 
z
Use any of various event actions that can set a variable on output using the function syntax: 
RV(PropertyName) 
Setting translatable captions for variables 
In the Inbox form’s Variable tab, the Caption column displays the contents of the notify or prompt 
message's variable captions in the current user’s language. This assumes that: 
z
The Caption component attributes are set to interpret the bound contents. 
z
The caption contains a translatable string name. 
For payload variables resulting from an IDO event, this string name might come from an IDO 
property’s label string ID. For non-payload variables that are created by an event action, you define 
this string name using the Event Actions form, Variable Access tab. 
The Saved Messages form 
The Saved Messages form displays messages that you have saved or at least have not yet deleted 
for a selected "folder." Within this folder, you can sort messages by any one of a number of criteria. 
For more information, see the online help for this form. 
You can also use this form to: 
z
Create your own "folders" for messages you want to save. 
z
Move messages from one folder to another. 
For more information, including the procedure to move messages, see the online help for the 
Folder Name field on this form. 
Folders, in this system, are not represented visually as they typically are in e-mail programs such 
as Outlook. The only place you can actually view your personal folders is in the Folder Name 
field on this form. For more information, including the procedure to create your own folders, see 
the online help for the Folder Name field.

You can also view messages on this form for information about any responses you might have made 
to messages generated by the system. 
Moving messages between folders 
You can use the Saved Messages form to move messages from one folder to another. If the folder 
does not already exist, you can create the folder at the same time. 
To move a message from one folder to another folder: 

Open the Saved Messages form. 

From the Folder Name drop-down list, select the folder in which the message you want to move 
is currently located. 
The system displays in the grid view all messages in that folder. 

In the grid view, select the message you want to move. 

In the Folder Name field, do one of these actions: 
z
For an existing folder, specify the name of the folder or select the folder from the drop-down 
list. 
z
To create a new folder and move the message to that folder, specify the name of the new 
folder. 

Save the message. 
The Send Message form 
The Send Message form is used to send system messages, similar to e-mail messages, to other 
users in the system. You can designate multiple recipients, "carbon-copy" recipients, and instruct the 
system whether to save a copy in your Sent Items "folder." 
For more information, including specific procedures and instructions for using this form, see the online 
help for this form. 
Sending e-mail to external e-mail Inbox for prompts 
If a user is set up in the Users form to allow the system to "send external prompts," then a prompt 
action sends the message both to the Mongoose Inbox form and to the recipient’s Inbox in an 
external e-mail client such as Microsoft Outlook. The message that is sent to the external e-mail 
system is an HTML-formatted e-mail that consists of these parts: 
z
Original subject in Subject line 
z
Category

z
List of internal recipients 
z
List of internal Cc recipients 
z
Original Body (either in plain text or HTML format) 
z
Original Question 
z
Choices, as individual hyperlinks to a .NET active server page (ASP) that records the vote 
z
Payload, which is the contents of the Variables grid from the Inbox 
Text in the Subject, Category, Body, Question, and Choices, as well as payload captions, can be 
translated and formatted based on the default language specified for the recipient user in the Users 
form. 
When the recipients vote by clicking the link in the e-mail, their Windows-default web browser opens 
or opens a new tab, as applicable, and sends the information from the link they clicked to the ASP 
URL that was included (and hidden) in the email. This URL is built by the system based on the web 
server list. 
The ASP then registers the vote programmatically, as if the recipient had logged into the system, 
displayed the same message in the Inbox, and selected the corresponding Choice button on the 
Response tab. 
The web page then displays a success or failure message. 
The message displays both in e-mail and in the Inbox form, but only one response is allowed: 
z
If users respond from e-mail first, when they display the Inbox (properly refreshed), the message 
is expired and the buttons are inactive. 
z
If users respond from the Inbox first, then clicking a link in the external e-mail brings up the web 
page with a message that the message has expired and they already voted, using the previously 
selected choice. 
Prompts and responses 
If a message is the result of a Prompt action, the sender of that message can request a specific 
response from each recipient, usually in the form of a button-vote mechanism. In such cases, the 
system must be set first to wait for responses, then to know how to handle responses as they are 
received, and finally, be instructed what to do when responses are not received within a specified 
timeout period. 
Incoming prompts request a response from recipients (using the Question field on the Inbox form or 
the external e-mail) and display a set of choices. The choices are displayed in the form of voting 
buttons in the Response tab area of the Inbox form, or in the form of links in an external e-mail. For 
example, a prompt might include buttons or links labeled: 
z
Approve / Disapprove (default option) 
z
Yes / No 
z
OK / Send More Info / Cancel

To customize the choices for a prompt, you must include a Prompt action with a Choices parameter 
as part of the event action definition. This Choices parameters consists of the CHOICES function 
followed by a string expression that evaluates to a comma-separated list that contains an even 
number of elements (value/label pairs). For example, if you want the voting buttons to be labeled Yes 
and No, with corresponding values returned to the action to be 1 and 0, you could include this 
parameter: 
CHOICES("1,sYes,0,sNo") 
In this example, the strings "sYes" and "sNo" are WinStudio form strings. These have already been 
defined for the system as Yes and No, respectively. 
If you want your button labels to be localized, for the recipient, you must: 
z
Use names of existing form strings (as found in the Strings table). 
OR 
z
Add your own form strings, using the Strings form, and provide the necessary translations. (To 
open the Strings form, you must be in Design Mode and, from the Edit menu, select Strings.) 
If localization is not an issue, you can also use a literal value that displays on the button verbatim. To 
specify the string as a literal value here, simply specify it as a list value. If the system does not find the 
string in the Strings table, the system automatically treats it as a literal value. 
See “Event action parameters” on page 126. 
Voting rules 
When a prompt is sent to a single recipient, the result of the prompt is the return value from that 
recipient's choice. However, when a prompt is sent to multiple recipients, you must select a vote-
counting method to determine the result of the prompt and include a Voting Rule parameter in your 
event action definition.

This table lists and describes the available voting rules.  
Rule 
Description 
Majority 
A choice must receive more than 50% of the vote to win. 
As soon as more than 50% of the recipients respond with a 
particular choice, that choice wins. 
If you use this voting rule, you should use a Voting Tie parameter 
(VOTINGTIE) to tell the system how to handle a tied vote. 
See “Dealing with indeterminate voting results” on page 65. 
Plurality 
The choice with the highest number of votes wins, even if it does 
not receive more than 50% of the vote. 
For example, if three choices are offered, and: 
The first choice receives 24% of the vote; 
The second choice receives 43% of the vote; and 
The third choice receives the remaining 33% of the vote; 
the second choice wins, even though it received less than 50% of 
the total vote. 
If you use this voting rule, you should use a Voting Tie parameter 
(VOTINGTIE) to tell the system how to handle a tied winning vote. 
See “Dealing with indeterminate voting results” on page 65. 
ConditionalPlurality 
The choice with the highest number of votes wins, but only if a 
specified minimum percentage of votes is reached. 
If you use this rule, you must also include a Minimum Percentage 
(MINIMUM) parameter. 
For example, if three choices are offered to 19 recipients, and you 
specify a minimum of 40% to win, then: 
In an 8-7-4 split, the choice with 8 votes would win because it 
meets the minimum percentage. 
In a 7-6-6 split, there would be no winner, because no choice meets 
the minimum percentage. In this case, the system must deal with 
the vote as an indeterminate result. 
See “Dealing with indeterminate voting results” on page 65. 
(In contrast, with a simple Plurality vote, the choice that reaches 7 
votes in a 7-6-6 split would win.) 
If you use this voting rule, you should use a Voting Tie parameter 
(VOTINGTIE) or Voting Disparity parameter 
(VOTINGDISPARITY) to tell the system how to handle the 
indeterminate vote. 
See “Dealing with indeterminate voting results” on page 65.

MinimumCount 
The first choice to reach a specified minimum number of votes 
wins. 
If you use this rule, you must also include a Minimum Count 
(MINIMUM) parameter. 
For example, if three choices are offered to 13 recipients, and you 
specifiy a minimum of 5 votes to win, the first choice to receive 5 
votes automatically wins. 
Note that, as soon as the minimum count is reached, event 
execution moves immediately to the next action. In this case, the 
system expires any responses not yet received, and no further 
voting can take place. 
MinimumPercentage 
The first choice to receive a specified percentage of the vote wins. 
The percentage is based on the number of recipients of the prompt, 
not the number of respondents. 
If you use this rule, you must also include a Minimum Percentage 
(MINIMUM) parameter. 
Note that, as soon as the minimum percentage is reached for a 
choice, event execution moves immediately to the next action. In 
this case, the system expires any responses not yet received, and 
no further voting can take place. 
EarliestResponse 
The first response to the prompt wins, regardless of the choice. 
Note that, as soon as the first response is received, event 
execution moves immediately to the next action. In this case, the 
system expires any responses not yet received, and no further 
voting can take place. 
PreferredChoice 
If any one respondent votes for the preferred choice, that choice 
wins. In a case where none of the respondents select the preferred 
choice, then this rule behaves like the Plurality rule for the 
remaining choices. 
If you use this rule, you must also include a Preferred Choice 
(PREFCHOICE) parameter to specify which choice is the preferred 
choice. 
For example, if you have three choices, and you specify the first 
choice as the preferred choice, then: 
If anyone votes for the first choice, that choice wins. 
If the end vote is a 0-6-5 split, the second choice wins. 
Note that, as soon as the preferred choice receives a vote, event 
execution moves immediately to the next action. In this case, the 
system expires any responses not yet received, and no further 
voting can take place. 
Rule 
Description

Dealing with indeterminate voting results 
These example situations create "indeterminate" voting results and set action attributes that are 
exposed as event functions that can be evaluated by subsequent event actions: 
z
Any disagreement among multiple recipients, registered as soon as a disagreement is detected. 
This can include a vote like the example offered in the Plurality description above. 
The associated event function is the VOTINGDISPARITY( ) event function, which is a Boolean 
function that indicates only that there was a disagreement. 
z
A tie in the case of a Plurality or Majority vote, registered at the point when all responses have 
been received or when the timeout period has expired. 
The associated event function is the VOTINGTIE( ) event function, which is a Boolean function 
that indicates only that there was a tie. 
You can use the returns from these functions, along with the functions RECIPIENTS( ), 
RESPONDERS( ), RECIPIENTLIST( ), RESPONDERLIST( ), and NONRESPONDERLIST() to take 
further actions, such as: 
z
Reprompting all the recipients and try to get a consensus. 
z
Reprompting only a select group of the respondents and urging them to adopt a different choice. 
z
Reprompting only recipients who have not yet responded. 
MinimumCountPreferred
Choice 
If a specified number of votes for a specified choice is cast, that 
choice wins. If you use this rule, you must also include a Minimum 
(MINIMUM) parameter to specify the minimum count, and a 
Preferred Choice (PREFCHOICE) parameter to specify which 
choice is the preferred choice. For example, if you set the 
Minimum to “3” for a Preferred Choice of "Approve," and 3 
recipients respond with "Approve," the preferred choice wins.  If 
fewer than that number of votes are cast for that choice after all 
recipients have responded, the vote reverts to Plurality. (In that 
case, the preferred choice can still win.)  Note that when you set 
the Minimum to 1, this rule behaves exactly like Preferred Choice. 
MinimumPercentage
PreferredChoice 
If a specified percentage of votes for a specified choice is cast, that 
choice wins. If you use this rule, you must also include a Minimum 
(MINIMUM) parameter to specify the minimum percentage, and a 
Preferred Choice (PREFCHOICE) parameter to specify which 
choice is the preferred choice. 
For example, if you set the Minimum to “25%” for a Preferred 
Choice of "Approve," and 2 of 8 of recipients respond with 
"Approve," the preferred choice wins.  If less than that percentage 
of votes are cast for that choice after all recipients have responded, 
the vote reverts to Plurality. (In that case, the preferred choice can 
still win.) 
Rule 
Description

z
Taking some other predetermined action. 
Quorums
On a Prompt action, a quorum is automatically calculated based on the number of recipients, the 
voting rule, and voting parameters such as Minimum.  If there is a number of votes by whose tally a 
voting result can be determined unambiguously, that number is the quorum.  Otherwise, the quorum 
is the number of recipients, that is, everyone has a chance to vote unless a timeout expires. As soon 
as the quorum is reached, voting is closed, any remaining unvoted messages are expired, and the 
event continues to the subsequent event action. 
However, if you specify a Quorum value, that overrides the automatic calculation. For example, if a 
message requiring a response is sent to 10 people, but you want a quorum to be reached when only 
4 have voted, then specify 4 as the Quorum value. 
By default, if Quorum is not specified or is specified with a positive value, Wait for Quorum is true; 
that is, the event waits until the quorum is reached before it continues with the next event action. If 
Quorum is specified with a non-positive value, the Wait for Quorum default value is FALSE. If these 
settings conflict, for example Quorum = 3 and Wait for Quorum is FALSE, the system displays an 
error message. 
If Wait for Quorum is FALSE, the event does not wait for a quorum to be reached. As soon as the 
messages are sent, execution continues with the next event action. If the system is not waiting for a 
quorum, the event designer needs to determine when a quorum is reached and what further actions 
to take. This can be done using VOTINGRESULT(), RESPONDERS(), RECIPIENTS(), etc., in 
combination with the Wait or Sleep actions.

### Appendix A: Sample Scenarios
*Pages 67-118*

A
Appendix A: Sample Scenarios
This appendix presents a number of typical scenarios in which you might want to use the Application 
Event System to automate various tasks in response to various situations. In each case, the situation 
is described and then a proposed solution involving events, handlers, and/or triggers. These solutions 
are presented in a step-by-step format, as examples that you can learn from and possibly modify for 
your own use.
Note: 
z
To a certain extent, each scenario builds on the concepts and practices of previous scenarios, so 
the most effective way to use them is to work through them sequentially. However, each scenario 
is also more-or-less "self-contained" and can be used independently of the others. 
z
To see a graphical representation for each flow as you work on it, you can use the Diagram 
button on the Event Handlers form. This button opens the Event Handler Diagram form, which 
you can use to view the flow of the event handler as well as access the Event Actions form to 
edit individual actions. For more information, see the online help for the Event Handler Diagram 
form. 
This list is a list of the scenarios included in this appendix: 
Sending notifications 
z
Scenario 1: Notification of a new record—adding a user on page 68 – A simple notification is 
sent to a credit manager when a new customer is added to the database. 
z
Scenario 2: Notification of changes to an existing record—changing the credit limit on page 74 
– The credit manager is notified by e-mail that a customer’s credit limit has been changed and 
is told what the new credit limit is. 
z
Scenario 3: Notification that includes an "old" value on page 78 – A group of inventory 
stockers are automatically notified whenever an item’s lot size changes. In the message that 
is sent, both the previous lot size and the new lot size are included.
Requesting approvals 
z
Scenario 4: Approval for a new record on page 84 – A purchasing manager is prompted for 
approval whenever a new purchase order is requested.

z
Scenario 5: Requesting approval by external e-mail for changes to an existing record on page 
90 – A credit manager is prompted through an external e-mail for approval of a change to a 
customer’s credit limit. 
z
Scenario 6: Requesting multiple and complex approvals on page 97 – A purchasing manager 
is prompted for approval on a purchase order (PO) both of a change in status to Ordered and 
for the amount of the PO. If the PO is for an amount greater than $100,000, a supervisor is 
also prompted for approval. If the PO is for an amount greater than $1,000,000, two senior-
level executives must also approve it. 
Modifying records 
z
Scenario 7: Adding information to a record on page 109 – A credit manager is prompted to 
provide a credit limit for a new customer, by means of a response to a message. 
Voting
z
Scenario 8: Voting for various choices on page 111– Several managers are prompted to 
approve an engineering change, by means of a response to a message. 
Localizing message contents
z
Scenario 9: Translating captions in a purchase request on page 113 – A message containing 
localizable strings is created. 
More advanced scenarios 
z
Scenario 10: Opening a session in a remote environment on page 115 – A remote site or 
Mongoose environment is accessed to retrieve data. The details of and procedure for this 
scenario are in the Integrating IDOs with External Applications guide. 
z
Scenario 11: Cross-site event firing - adding a message to another site's Inbox on page 116 – 
A message is sent to another site’s Inbox form by using a GenericNotify event.
Sending notifications 
One of the simplest uses of the event system is to set up situations in which message notifications are 
sent out automatically to specified individuals whenever a situation occurs or a condition is met. The 
scenarios in this section illustrate this kind of situation. 
Scenario 1: Notification of a new record—adding a user 
Suppose you have a system administrator who wants to be notified whenever a new user is added to 
the system, regardless of who adds the user. Of course, you can simply require each employee who

adds users to the system to manually send a notice whenever a user is added. But that places an 
additional burden on the employee and is prone to possible oversight. 
A simple event and handler 

added. In this example, you do not need to create an event, because Infor provides an event named 
IdoPostItemInsert that you can use. All you need to do is create an event handler for that event and 
assign an action to it that generates and sends the message to the system administrator. 
We could use the IdoOnItemInsert framework event instead of the IdoPostItemInsert event. This will 
be significant when we get to the section on  Refining the message on page 71. The advantage of 
using the IdoPostItemInsert event is that, if you allow the Users form to auto-assign the user ID 
number (instead of specifying the user ID number yourself), the system waits until the ID number has 
been assigned before filling in the "CustNum" data in the message. If we use the IdoOnItemInsert 
event, the system does not wait, which means that, if you auto-assign the customer ID number, the 
restulting message has "TBD" in place of the actual customer number. 
To set this up: 
1.
Create the event handler: 
a.
Open the Event Handlers form. 
b.
Press F3. 
c.
Press Ctrl+N. 
d.
Create the handler with these settings:  
Field or Option 
Setting / Comments 
Event Name 
From the drop-down list, select IdoPostItemInsert. 
Note: For details about this and the other 
framework events included with the system, see 
“Framework events” on page 122. 
Applies to Initiators 
Leave blank. 
Applies to Objects 
Specify SLCustomers. 
To determine what object you need, see the 
procedure provided in the online help for this field. 
Keep With 
Leave blank. 
Chronology 
Leave blank. 
Ignore Failure 
Cleared. 
Suspend 
Cleared.

For more information about any of these fields and options, see the help for the Event 
Handlers form. 
e.
Save. 
2.
Define the action for the event handler you just created: 
a.
In the Event Handlers form, select the handler you created in Step 1. 
b.
Click Event Actions. 
c.
In the Event Actions form, in the Action Sequence field, specify 10. 
d.
From the Action Type drop-down list, select Notify. 
e.
Click Edit Parameters. 
f.
In the Event Action Notify form, click the To button. 
g.
In the Event Action Parameter Recipients form, from the list of recipients, select the user ID 
of the credit manager (or whoever is serving in that role).  
h.
Click Update and then OK. 
i.
In the Subject field, specify New Customer! 
j.
In the Category field, specify Change Notification.
k.
In the Body field, specify We have a new customer! 
Synchronous 
Cleared. 
Because this notification does not require any 
response from the credit manager, it can run 
asynchronously. For more information, see 
“Synchronicity” on page 16. 
Active 
Selected. 
Can Override 
Selected. 
Transactional 
Cleared. 
Obsolete 
Cleared. 
Initial State 
Leave blank. 
Initial Action 
Leave blank. 
Note: Technically, you can specify any integer you want in this field, and the 
system treats them sequential order. We recommend using multiples of ten, 
initially at least, just in case you later need to add more action steps between 
existing steps, so you do not need to renumber all existing steps. 
TIP: You can select more than one recipient. Also, to deselect a recipient, click 
the user ID again. 
Field or Option 
Setting / Comments

l.
Select the Save in Sent Items check box. 
This parameter tells the system to save a copy of the notification in the Sent Items folder of 
the person who added the new customer. 
m. Click OK. 
On the Event Actions form, in the editable field on the Parameters tab, you should see this: 
CATEGORY("Change Notification")
TO("userID") 
SUBJECT("New Customer!") 
BODY("We have a new customer!") 
SAVEMESSAGE(TRUE) 
where userID is the sign-in user ID for the credit manager.  
3.
(Optional, but recommended) To verify that there are no syntax errors, click Check Syntax. 
4.
Save the action and close the Event Actions form. 
5.
Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Test the event by using the Customers form to create a new customer. Then, sign in as the user ID 
specified in the TO parameter, open the Inbox form, and verify that the message was received. The 
message should appear there, along with the properties associated with the new customer, on the 
Variables tab. Note that, because you did not specify any variable access rules, all properties 
(variable values) are display-only. 
Refining the message 
Suppose you now want to refine the message, to make it even more informative and useful to the 
recipient. Not only do you want the recipient to get a message, but you want that message to include 
the customer number and name for the new customer, so the recipient can look up the customer 
profile more easily. 
To include the customer number and name in the message: 
1.
In the Event Handlers form, select the handler you just created and then click Event Actions. 
2.
In the Event Actions form, click Edit Parameters. 
3.
In the Event Action Notify form, click the Body button. 
4.
In the Event Action Expression Editor form, from the Select a function drop-down list, select 
SUBSTITUTE. 
TIP: Note where double quotation marks and parentheses are inserted. Because 
it can be confusing to know where and when to use these punctuation marks, 
we recommend that you use the event action parameter forms as described 
in these scenarios. They insert the correct punctuation marks automatically 
where and when needed and can help you avoid many time-consuming 
errors in syntax.

The SUBSTITUTE function allows you to specify the basic text of a message, with "replacement 
markers" embedded in the message. At run time, the system substitutes specified values for 
these replacement markers. This effectively allows you to create messages with dynamic content. 
5.
In the Argument 1 field, specify We have added a customer, {0}, customer ID {1}, to our 
family of customers. 
The numbers enclosed in curly braces ( {0} and {1} ) are the replacement markers for which 
values will be substituted at run time.  
6.
Create the expression that will be used to supply the value for replacement marker {0}: 
a.
Place the cursor in row 1 of the Arguments grid and then click Build Expression. 
b.
In the Event Action Expression Editor form, from the Select a function drop-down list, 
select PROPERTY. 
c.
The PROPERTY function picks up the value of the CustNum (Customer Number) field. 
d.
In the Argument 1 field, specify Name and then click OK. 
7.
Repeat Step 6 for row 2, using CustNum for the PROPERTY argument (propertyname) in 
substep d. 
8.
In the Event Action Notify form, click OK. 
9.
(Optional) On the Event Actions form, click Check Syntax. 
10. Save the action and close the Event Actions form. 
11. Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Test by creating a new customer record and verifying that the intended recipient receives a 
notification message that includes the correct new customer name and number. 
Refining the recipient 
When defining the recipients for this message, it can be a good idea to use a global constant value, 
rather than a hard-coded user ID. This allows you to use the same global constant value in other 
places in your application. Then, if the name of the credit manager changes, for instance, it is 
possible to change the recipients by simply changing the global constant value. It also allows you to 
add multiple recipients, for instance, if you have co-credit managers or you have a trainee you want to 
also receive the messages. 
Note: Replacement markers must be enclosed in curly braces { }. They must begin 
with zero (0) and increment sequentially. If you do not begin with zero or you skip 
integers, they do not work. 
Note: What if you do not know the name of the property for which you want to 
retrieve a value? How do you find that property name? For an easy method to find 
the property name, see “Determining names of IDO collections and components” 
on page 48.

For more information about global constants, see “About event global constants” on page 42. 
To redefine the recipients as a global constant: 
1.
Create the global constant: 
a.
Open the Event Global Constants form and take it out of filter-in-place mode. 
b.
In the Name field, specify the name to assign to the constant. 
c.
In this case, you might use CreditMgr. 
d.
In the Value field, specify the logon user ID for the credit manager.  
e.
Save the global constant and close the form. 
2.
Incorporate the global constant in the event handler action: 
a.
In the Event Handlers form, select the handler and then click Event Actions. 
b.
In the Event Actions form, click Edit Parameters. 
c.
In the Event Action Notify form, click the To button. 
d.
In the Event Action Parameter Recipients form, click the Recipients button. 
e.
In the Event Action Expression Editor form, from the Select a function drop-down list, 
select GC. 
The GC function calls a specified global constant and uses its value at run time. In this case, 
you want the global constant you created in Step 1. 
f.
From the Argument 1 drop-down list, select the global constant you created in Step 1 
(CreditMgr) and then click OK. 
Notice that the global constant name is not enclosed in double quotation marks. Generally, 
only literal strings and property names must be enclosed in double quotation marks. 
g.
In the Event Action Parameter Recipients form, click OK. 
h.
In the Event Action Notify form, click OK. 
i.
To verify that there are no syntax errors, click Check Syntax. 
j.
(Optional) On the Event Actions form, click the Substituted Parameters tab and notice that 
the TO parameter indicates the actual recipient; in other words, the value of the global 
constant. 
k.
Save the action and close the Event Actions form. 
Test by creating a new customer record and verifying that all designated recipients receive the 
notification message. You can also check the Saved Messages form for the user ID from which you 
were signed in when the message was sent. 
Note: To add multiple recipients, specify the user IDs separated by semi-colons 
only—no spaces.

Points to note and remember 
In creating this kind of event handler, keep these points in mind: 
z
If you do not require a response from the recipient, create the handler as an asynchronous 
handler, to avoid system slow-downs. 
z
To be able to use a recipient in other handlers and be able to change that recipient when 
necessary in only one place, use an event global constant for the recipient. 
z
To use active data in a message, use the SUBSTITUTE and PROPERTY (or P) function 
constructs. 
Scenario 2: Notification of changes to an existing record—changing the 
credit limit 
This scenario is similar to the first one, except that, instead of notifying the credit manager when a 
customer is added to the database, we want to create an event and handler that notifies the credit 
manager whenever a customer’s credit limit is changed. Because the credit manager prefers email 
and is not always signed in to the system, we also want to send the notification as an e-mail. 
Note: For this scenario to work properly, you must have SMTP enabled and configured on the 
Intranets form of the utility server. You must also have your SMTP server set up to relay the e-mails 
that are sent. For information on how to do this, consult your Windows operating system 
documentation. Finally, any recipients must also have e-mail addresses saved as part of their user 
profiles. 
As with the first scenario, we can use an existing framework event, IdoOnItemUpdate, and create our 
own handler for it. And again, because we are simply sending out a notification and the system is not 
waiting for a response from the credit manager, we can make it an asynchronous event handler. 
This event handler requires two actions: one to check whether the Credit Limit field has been 
changed and one to send the e-mail notification. 
To accomplish this scenario: 
1.
Create the event handler: 
a.
Open the Event Handlers form. 
b.
Press F3. 
c.
Press +N. 
d.
Create the handler with these settings:  
Field or Option 
Setting / Comments 
Event Name 
From the drop-down list, select IdoOnItemUpdate. 
NOTE: For details about this and the other framework events 
included with the system, see “Framework events” on 
page 122. 
Applies to Initiators 
Leave blank.

For more information about any of these fields and options, see the online help for the Event 
Handlers form. 
e.
Save the handler. 
2.
Create the first action, which checks the condition of the Credit Limit field when the customer 
record is saved: 
a.
In the Event Handlers form, select the handler you just created. 
b.
Click Event Actions. 
c.
In the Event Actions form, in the Action Sequence field, specify 10.
d.
From the Action Type drop-down list, select Finish. 
This action type tells the system to finish executing the handler when a particular condition 
has been met and exit. 
e.
Click Edit Parameters. 
f.
In the Event Action Finish form, click the Condition button. 
g.
In the Event Action Parameter Condition form, click the Expression 1 button. 
Applies to Objects 
Specify SLCustomers. 
To determine what object you need, see the procedure 
provided in the online help for this field. 
Keep With 
Leave blank. 
Chronology 
Leave blank. 
Ignore Failure 
Cleared. 
Suspend 
Cleared. 
Synchronous 
Cleared. 
Because this notification does not require any response from 
the credit manager, it can run asynchronously. For more 
information, see “Synchronicity” on page 16. 
Active 
Selected. 
Can Override 
Selected. 
Transactional 
Cleared. 
Obsolete 
Cleared. 
Initial State 
Leave blank. 
Initial Action 
Leave blank. 
Field or Option 
Setting / Comments

h.
In the Event Action Expression Editor form, from the Select a function drop-down list, 
select the function PROPERTYMODIFIED. 
The PROPERTYMODIFIED function checks to see whether the named property has been 
modified since the last save. If the property has been modified, the expression returns a value 
of TRUE. 
i.
In the Argument 1 field, specify CreditLimit, which is the name of the property that we want 
to check. 
j.
Click OK. 
Notice in the Event Action Parameter Condition form that the expression has been returned 
and that double quotation marks have been automatically inserted around the name of the 
property. 
Notice also that the Operator and Expression 2 fields have been disabled. This is because 
the PROPERTYMODIFIED function is a Boolean expression; thus, no comparison is needed 
to return a Boolean value. 
k.
Select the NOT check box. 
The reason you select this option is because, if you did not, the expression would return a 
value of TRUE whenever the CreditLimit property has been modified and the handler would 
finish. But you want the system to continue to the next action when the CreditLimit property 
has been modified; you want the system to finish at this point only if the CreditLimit property 
has not been modified. 
l.
Click OK. 
Notice that the system returns the expression to the Event Action Finish form correctly 
formatted. 
m. Click OK. 
Notice that the system returns the entire parameter to the Event Actions form with the syntax 
correctly formatted. 
n.
To verify that the syntax is correct, click Check Syntax. 
o.
Save the action. 
3.
Create the second action, which sends the e-mail notification: 
a.
To create the action, press Ctrl+N. 
b.
In the Action Sequence field, specify 20.
c.
From the Action Type drop-down list, select Send Email and then click Edit Parameters. 
d.
In the Event Action Send Email form, click the To button. 
e.
In the Event Action Parameter Recipients form, select the user ID for the credit manager. 
Note: What if you do not know the name of the property for which you want to retrieve 
a value? How do you find that property name? For an easy method to find the 
property name, see “Determining names of IDO collections and components” on 
page 48.

If the credit manager has an e-mail address set up as part of the user profile, the e-mail 
address displays to the right of the user ID. If the credit manager’s user ID does not display an 
e-mail address, you must add the e-mail address to the credit manager’s user profile on the 
Users form. 
Notice that you could again use a global constant for the credit manager’s e-mail address. 
However, because we are sending e-mail, we cannot reuse the existing CreditMgr global 
constant, but must create a new global constant for the credit manager’s e-mail address. The 
reason for not using an event global constant in this case was simply to give you some 
experience with the Event Action Parameter Recipients form’s other capabilities. (In most 
scenarios, a global constant will be used.) 
f.
Click Update. 
Notice that the system places the e-mail address for the credit manager in the Recipients 
field. 
g.
Click OK. 
h.
In the Subject field, specify: Credit limit change 
i.
In the Category field, specify: Financial 
j.
Click the Body button. 
k.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
SUBSTITUTE. 
l.
In the Argument 1 field, specify: The credit limit has been changed to ${0} for customer 
{1}, customer number {2}. 
m. Place the cursor in the first row of the Arguments grid, and click Build Expression. 
n.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
FILTERPROPERTY. 
o.
In the Argument 1 field, specify CreditLimit and click OK. 
p.
Place the cursor in the second row of the Arguments grid, and click Build Expression. 
q.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
FILTERPROPERTY. 
r.
In the Argument 1 field, specify Name and click OK. 
s.
Place the cursor in the third row of the Arguments grid, and click Build Expression. 
t.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
FILTERPROPERTY. 
u.
In the Argument 1 field, specify CustNum and click OK. 
v.
Click OK. 
Notice that the system returns the entire SUBSTITUTE expression to the Event Action Send 
Email form, correctly formatted. 
Notice also that there is no option to save the message to the user’s Sent Items folder. This is 
because this notification is being sent as an e-mail. That being the case, we cannot use the

SAVEMESSAGE parameter to have the system save a copy of the notification in the Sent 
Items folder of the person who added the new customer. 
w. Click OK. 
x.
Save the action and close the Event Actions form. 
4.
Verify that you have no syntax errors by clicking Check Syntax. 
5.
Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Test this event handler by changing a customer’s credit limit and saving the record. The system 
should generate an e-mail message that gets sent to the credit manager. 
Points to note and remember 
In creating this kind of event handler, keep these points in mind: 
z
To create an event handler that sends an e-mail, you must have the SMTP set up on the 
Intranets form. Also, the e-mail service on that computer must be set up to enable the relaying of 
e-mail automatically. 
z
To have the handler do something only when certain conditions are met, use the Finish action 
type and the CONDITION(NOT PROPERTYMODIFIED) parameter and function. 
z
To eliminate the single quotes that appear around replacement values in the generated 
messages, use the PROPERTY function in place of the FILTERPROPERTY function we used in 
this scenario. 
Scenario 3: Notification that includes an "old" value 
In this scenario, we want to notify a group of inventory stock clerks automatically whenever an item’s 
lot size changes. In the message that is sent, we want to include both the previous lot size and the 
new lot size. We also want to let them know who initiated the change. 
Once again, we will use an existing framework event, IdoOnItemUpdate, and create our own handler 
for it. Because this handler needs to retrieve the "before" property values, we must make it 
synchronous, so that during handler execution we can retrieve from the database the original row that 
is being updated, before it is updated by the IDO request. 
This event handler requires three actions: 
z
One to check whether the Lot Size field has been changed and, if not, finish. 
z
One to retrieve the row being updated and both the original and new values for the Lot Size field. 
z
One to send the notification to the inventory stock clerks. 
To accomplish this scenario: 
1.
Create the event handler: 
a.
Open the Event Handlers form. 
b.
Press F3.

c.
Press Ctrl+N. 
d.
Create the handler with these settings:  
e.
Save the handler. 
2.
Create an event global constant for the group of stock clerks. 
Putting the user IDs for the entire group into a global constant allows us to change the list, which 
might be used in other places as well, in a single place easily. 
a.
Open the Event Global Constants form. 
b.
Press F3 or F4. 
c.
Press Ctrl+N. 
d.
In the Name field, specify the name for the global constant, in this case, StockClerks. 
Field or Option 
Setting / Comments 
Event Name 
From the drop-down list, select IdoOnItemUpdate. 
Note: For details about this and the other framework events 
included with the system, see “Framework events” on page 122. 
Applies to Initiators 
Leave blank. 
Applies to Objects 
Specify SLItems. 
To determine what object you need, see the procedure provided in 
the online help for this field. 
Keep With 
Leave blank. 
Chronology 
Leave blank. 
Ignore Failure 
Cleared. 
Suspend 
Cleared. 
Synchronous 
Selected. 
Because this notification requires both the original value and the 
new value, it must be run synchronously. For more information, 
see “Synchronicity” on page 16. 
Active 
Selected. 
Can Override 
Selected. 
Transactional 
Cleared. 
Obsolete 
Cleared. 
Initial State 
Leave blank. 
Initial Action 
Leave blank.

e.
In the Value field, specify the user IDs for the stock clerks, separated only by semi-colons (;) 
and no spaces. 
f.
Save, and close the form. 
3.
Create the first action, which checks the condition of the Lot Size field when the item record is 
saved: 
a.
In the Event Handlers form, select the handler. 
b.
Click Event Actions. 
c.
In the Event Actions form, in the Action Sequence field, specify 10.
d.
From the Action Type drop-down list, select Finish. 
e.
Click Edit Parameters. 
f.
In the Event Action Finish form, click the Condition button. 
g.
In the Event Action Parameter Condition form, click the Expression 1 button. 
h.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
PROPERTYMODIFIED. 
i.
In the Argument 1 field, specify LotSize and then click OK. 
j.
In the Event Action Parameter Condition form, select the NOT check box and then click 
OK. 
k.
In the Event Action Finish form, click OK. 
This parameter tells the system to check the LotSize property. If it has not been modified, 
finish handler execution and exit. If it has been modified, continue with the second action. 
l.
Save the action. 
4.
Create the second action, which retrieves both the original and new values for the Lot Size field. 
As part of this step, the system retrieves the original value of the Lot Size field and stores the 
value to an event variable named OldLotSize. 
For this action type to work, you must: 
z
Use the IDO( ) function to identify the same IDO that fired the event. 
z
Name the same property in the PROPERTIES( ) and SET( ) functions, and both should be the 
same as the field/component property value the user is changing. 
z
Make sure the handler is synchronous. 
To create the action: 
a.
Press Ctrl+N. 
b.
In the Action Sequence field, specify 20. 
Note: What if you do not know the name of the property for which you want to 
retrieve a value? How do you find that property name? For an easy method to find 
the property name, see “Determining names of IDO collections and components” 
on page 48.

c.
From the Action Type drop-down list, select Load IDO Row. 
d.
Click Edit Parameters. 
e.
In the Event Action Load IDO Row form, the IDO field, specify: SLItems 
f.
In the Properties field, specify LotSize. 
g.
Click the Filter button. 
h.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
SUBSTITUTE. 
i.
In the Argument 1 field, specify: Item = {0} 
j.
Place your cursor in the first Arguments row and then click Build Expression. 
k.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
FILTERPROPERTY. 
l.
In the Argument 1 field, specify Item and then click OK. 
m. Click OK. 
n.
Click the Output button. 
o.
In the first row of the Event Action Output Parameters form, from the Output Type drop-
down list, select Return Variable. 
p.
In the Output Object Name field, specify: OldLotSize 
q.
In the Value field, specify LotSize and then click OK. 
r.
In the Event Action Load IDO Row form, click OK. 
Your resulting syntax statement should appear like this in the Parameters field of the Event 
Actions form: 
IDO("SLItems") 
PROPERTIES("LotSize") 
FILTER(SUBSTITUTE("Item = {0}", FP("Item"))) 
SET(RV(OldLotSize) = "LotSize") 
s.
Verify that the action has no syntax errors. 
t.
Save the action. 
5.
Create the third action, which sends the notification: 
a.
To create the action, press Ctrl+N. 
b.
In the Action Sequence field, specify 30.
Note: You can also select the IDO you want from the drop-down list, but you 
might have to filter on the field or increase the record cap for drop-down lists to 
see this one. 
Also, the procedure for figuring out what IDO collection you need is similar to the 
procedure for figuring out what property name you need. For more information, 
see “Determining names of IDO collections and components” on page 48.

c.
From the Action Type drop-down list, select Notify. 
d.
Click Edit Parameters. 
Setting up the TO parameter: 
a.
In the Event Action Notify form, click the To button. 
b.
In the Event Action Parameter Recipients form, click Recipients. 
c.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
GC. 
The GC function allows you to designate an event global constant to use for the recipients. In 
this case, we will designate the global constant we created earlier, StockClerks. 
d.
From the Argument 1 drop-down list, select StockClerks and then click OK. 
e.
In the Event Action Parameter Recipients form, click OK. 
Setting up the CC, SUBJECT, and CATEGORY parameters: 
a.
Click Cc button. 
b.
In the Event Action Parameter Recipients form, click Recipients. 
c.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
ORIGINATOR. 
Notice that the ORIGINATOR function takes no arguments. 
d.
Click OK twice. 
e.
In the Subject field, specify: Lot size change 
f.
In the Category field,  specify: Change Notification 
Setting up the BODY parameter: 
a.
Click the Body button. 
b.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
SUBSTITUTE. 
c.
In the Argument 1 field, specify: The lot size has been changed for item: {1} The previous 
lot size was {2}, the new lot size is {3}. Please take note and adjust your activities 
accordingly. This change was made by {0}. 
d.
Place your cursor in the first row of the Arguments grid and then click Build Expression. 
e.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
ORIGINATOR and then click OK. 
Notice that we can place this first property (ORIGINATOR) last in the message, and, as long 
as we have the appropriate index number assigned ( {0} ), it will be correctly displayed in the 
message. 
f.
Place your cursor in the second row of the Arguments grid and then click Build Expression. 
g.
In the Event Action Expression Editor, from the Select a function drop-down list, select 
FP.

h.
From the Argument 1 drop-down list, select Item and then click OK. 
In this substep, because we want the item number to be enclosed in single quote marks, we 
use the FP (alternate for the FILTERPROPERTY) function. However, we do not want single 
quote marks around the lot size amounts, so we will let those values evaluate as their native 
datatypes. 
i.
Place your cursor in the third row of the Arguments grid and then click Build Expression. 
j.
In the Event Action Expression Editor, from the Select a function drop-down list, select V 
from the list of functions. 
k.
In the Argument 1 field, specify OldLotSize and then click OK. 
l.
Place your cursor in the fourth row of the Arguments grid and then click Build Expression. 
m. In the Event Action Expression Editor, from the Select a function drop-down list, select P 
(or PROPERTY) from the list of functions. 
n.
From the Argument 1 drop-down list, select LotSize and then click OK. 
o.
In the Event Action Expression Editor, click OK. 
The resulting syntax statement looks similar to this: 
BODY(SUBSTITUTE("The lot size has been changed for item: {1} The previous lot size 
was {2}, the new lot size is {3}. Please take note and adjust your activities accordingly. 
This change was made by {0}.",  
ORIGINATOR(), 
FP("Item"), 
V(OldLotSize), 
P("LotSize")) 
p.
In the Event Action Notify form, click OK. 
6.
Verify that you have no syntax errors. 
7.
Save the action and close the Event Actions form. 
8.
Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Testing the event handler 
To test this handler: 
1.
Open the Items form and locate an item that is lot-tracked. 
2.
On the General tab, change the value in the Lot Size field and save the record. 
3.
In the stockers’ Inbox forms, verify that the message was sent and contains the correct values. 
Note: If you want, you can add line returns to make your syntax statement look 
like this example. The system ignores white space and line returns when 
processing the statements.

Points to note and remember 
In creating this kind of event handler, keep these points in mind: 
z
To retrieve the previous (existing) value of a field for display in a message, you must make the 
handler synchronous. 
z
To display both the original value of a field and the new one, use an event variable to temporarily 
store the original value. 
z
Substituted values in a statement can be presented in any order as long as their index numbers 
match their positions in the list. 
z
To prevent single quotes from being placed around a substituted value, use the PROPERTY 
function instead of the FILTERPROPERTY function. 
Extra challenge 
Try on your own adding the item description to the body of the message. This might require you to 
determine the name of the item description property, if you do not already know it. For more 
information, see “Determining names of IDO collections and components” on page 48. 
Requesting approvals 
These two scenarios, which are similar, build on the concepts and practices used in the first two 
scenarios The big difference is that they both use the Prompt action type to ask a manager to approve 
some action. 
Note: Before trying these scenarios, we recommend that you go through the scenarios so far, if you 
have not already done so. These scenarios assume that you already know how to accomplish certain 
tasks without taking you through them in detail. 
Scenario 4: Approval for a new record 
In this scenario, we want to send a message to the purchasing manager whenever a purchase order 
(PO) is added. This message prompts the purchasing manager for approval of the PO. The 
purchasing manager can indicate approval (or disapproval) by clicking a button in the message itself. 
If approved, the system adds the PO; if not, the system does not add the PO. 
As with the previous scenarios so far, the system framework has a built-in event, IdoOnItemInsert, 
which we can use with our handler. The handler itself requires two actions: one to send the prompt, 
and one to tell the system what to do if approval is denied. 
To set the system up to handle this: 
1.
Create a global constant for the purchasing manager. 
a.
For the Name of the global constant, use PurchasingMgr. 
b.
For the Value field, specify the purchasing manager’s user ID.

Remember: To add multiple recipients, specify user IDs separated by semi-colons (;) and no 
spaces. 
2.
Create and save an event handler with these settings:  
Field or Option 
Setting / Comments 
Event Name 
From the drop-down list, select IdoOnItemInsert. 
Note: For details about this and the other framework events 
included with the system, see “Framework events” on 
page 122. 
Applies to Initiators 
Leave blank. 
Applies to Objects 
Specify SLPos. 
To determine what object you need, see the procedure 
provided in the online help for this field. 
Keep With 
Leave blank. 
Chronology 
Leave blank. 
Ignore Failure 
Cleared. 
Suspend 
Cleared. 
Because this notification does require a response from the 
purchasing manager, it must run synchronously and be 
suspended. 
However, we cannot select this (and make it "stick") until at 
least one adjourning action exists. So, we must leave this 
cleared for now and come back to it after our actions have 
been defined. 
For more information, see “Suspension” on page 18. 
Synchronous 
Doesn’t matter at this point. 
Because this notification does require a response from the 
purchasing manager, it must run synchronously and be 
suspended. When you later select the Suspend option, this 
will be automatically selected. 
For more information, see “Synchronicity” on page 16. 
Active 
Selected. 
Can Override 
Selected. 
Transactional 
Cleared. 
Obsolete 
Cleared. 
Initial State 
Leave blank. 
Initial Action 
Leave blank.

For more information about any of these fields and options, see the online help for the Event 
Handlers form. 
3.
Create the first action, to send the message: 
a.
In the Event Actions form, in the Action Sequence field, specify 10.
b.
From the Action Type drop-down list, select Prompt and then click Edit Parameters. 
This action type not only sends a notification to the designated recipient, it also prompts the 
recipient for a response. 
c.
Starting with the Event Action Prompt form, use the associated forms to create these 
parameters: 
Field / Button 
Action 
Result / Comments 
To button
Click. 
The Event Action Parameter Recipients 
form opens. 
Recipients 
Click button. 
The Event Action Expression Editor opens. 
Select a function 
Select GC. 
The Argument 1 field and drop-down list 
display. 
Argument 1 
drop-down list 
Select PurchasingMgr. 
This is the global constant 
we created earlier. 
Click OK. 
The system returns the expression to the 
Event Action Parameter Recipients form. 
OK button
Click. 
The system returns the expression to the 
Event Action Prompt form. 
Subject field 
Specify: New purchase 
order needs your approval 
— 
Category field
Specify: Order Approval
—
Body button 
Click. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select SUBSTITUTE. 
The Argument 1 field and drop-down list, 
Arguments grid, and buttons display. 
Argument 1 field 
Specify: A new purchase 
order has been requested 
for vendor {0}, {1}.  Please 
review the details on the 
Variables tab and register 
your approval on the 
Response tab. 
— 
Arguments grid, 
row 1 
With cursor in the field, click 
Build Expression. 
The Event Action Expression Editor form 
opens.

Select a function 
Select P or PROPERTY. 
The Argument 1 field and drop-down list 
display. 
Argument 1 field 
Select VendNum and click 
OK. 
The system returns the expression to the 
parent Event Action Expression Editor. 
Arguments grid, 
row 2 
With cursor in the field, click 
Build Expression. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select P or PROPERTY. 
The Argument 1 field and drop-down list 
display. 
Argument 1 field 
Select VendorName and 
click OK. 
The system returns the expression to the 
parent Event Action Expression Editor. 
OK button 
Click. 
The system returns the entire BODY 
parameter content to the Event Action 
Prompt form. 
Question field 
Specify: Do you approve 
this new PO? 
Note that, when the handler runs, the 
QUESTION parameter is presented on the 
Response tab of the recipient’s Inbox. 
Choices button 
Click. 
The Event Action Prompt Choices form 
opens. 
Note that the CHOICES parameter creates, 
displays, and enables the voting buttons that 
will be required for the purchasing manager to 
signal approval or rejection. When the handler 
runs, these CHOICES buttons appear directly 
beneath the QUESTION in the recipient’s 
Inbox. 
Return Value 
field, row 1
Specify: 1 
Note that you can specify any value you want 
here. 
Button Caption 
field, row 1 
Specify: sYes 
Note that you can use translatable strings 
from the Strings table. These strings appear in 
the drop-down list for this field. 
Return Value 
field, row 2
Specify: 0 
— 
Button Caption 
field, row 2 
Specify: sNo 
— 
OK button 
Click. 
The system returns the choices data to the 
Event Action Prompt form. 
OK button 
Click. 
The system returns all defined parameters to 
the Event Actions form, correctly formatted. 
Field / Button 
Action 
Result / Comments

d.
Verify that there are no syntax errors. 
e.
Save the action. 
If you have done everything correctly, your syntax for this action step should look like this: 
TO(GC(PurchasingMgr)) 
SUBJECT("New purchase order needs your approval")
CATEGORY("Order Approval")
BODY(SUBSTITUTE("A new purchase order has been requested for vendor {0}, {1}.  Please 
review the details on the Variables tab and register your approval on the Response tab.", 
P("VendNum"), P("VendorName") ) 
SAVEMESSAGE(FALSE) 
QUESTION("Do you approve this new PO?") 
CHOICES("1,sYes,0,sNo") 
4.
Create the second action, which tells the system how to respond if approval is not granted: 
a.
In the Action Sequence field, specify 20.
b.
From the Action Type drop-down list, select Fail. 
This action type ends handler execution with an error status. This effectively aborts the 
process and prevents the PO from being added to the database. 
c.
Starting with the Event Action Fail form, use the associated forms to create these 
parameters:  
Field / Button 
Action 
Result / Comments 
Condition button
Click. 
The Event Action Parameter Condition form 
opens. 
Expression 1 
button 
Click. 
The Event Action Expression Editor opens. 
Select a function 
Select VOTINGRESULT. 
The Action drop-down list displays. 
This function and action evaluate the results 
of whatever action is selected from the list. 
The action refers by number to the action 
type. 
In this case, we have only one other action, 
and that is the correct action, the Prompt 
action. 
Action drop-down 
list 
Select 10 Prompt and click 
OK. 
The system returns the expression to the 
Expression 1 field on the Event Action 
Parameter Condition form. 
Operator drop-
down list 
Select = (equals). 
—

d.
Verify that there are no syntax errors and save the action. 
5.
Return to the Event Handlers form and select the Suspend check box. 
6.
Save the handler. 
7.
Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Testing the event handler 
To test this handler: 
1.
Open the Purchase Orders form, create a new purchase order, and save it. 
After you save the PO, when the Purchase Orders form refreshes the display, the new record 
should disappear from the display. It remains hidden until/unless it has been approved. 
If you do not assign a PO number, the generated message displays it with a PO number of TBD. 
2.
Open the Inbox form for the individual designated as the Purchasing Manager and verify that the 
message was received and that the Response tab displays the question and choice buttons. 
3.
(Optional) With the Purchase Orders form selected, from the Actions menu, select View Event 
Status. 
This opens the Event Status form. Navigate to the last row and verify that the status for this event 
is Running. 
4.
In the Inbox form, click the button labeled Yes. 
5.
Refresh the collection on the Purchase Orders form and verify that the new PO now displays in 
the list. 
You can also do a second test, clicking the button labeled No to reject the request. In this case, when 
you refresh the Purchase Orders form, the new PO record is never added to the database and does 
not appear in the list of POs. 
Expression 2 field 
Specify: 0 (zero) and click 
OK. 
This value tells the system to fail the handler 
with an error if the recipient responds with a 
"No" (0). 
The system returns the entire condition 
statement to the Event Action Fail form. 
Result field 
Specify: The PO request 
was rejected by the 
purchasing manager. 
This message appears on the Event Status 
form if the purchasing manager responds with 
a "No." 
OK button 
Click. 
The system returns both parameters to the 
Event Actions form, correctly formatted. 
Field / Button 
Action 
Result / Comments

Points to note and remember 
When creating this kind of event handler, keep these points in mind: 
z
When creating a message that requires a response from the recipient (usually a Prompt action 
type), you must mark the handler so that it suspends when executed. This means that it is also 
automatically marked as a synchronous handler. 
z
Because these event handlers must be suspended, pending the purchasing or credit manager’s 
response, the Framework Event Service must be enabled for the configuration in which you are 
logged on. 
Extra challenge 
Try changing the Subject line so that it displays the user ID of the person who created the new PO 
and the PO number. 
Hint: You will need to use the SUBSTITUTE function. 
Scenario 5: Requesting approval by external e-mail for changes to an 
existing record 
This scenario is similar to the one in Scenario 2: Notification of changes to an existing record—
changing the credit limit on page 74, except that in this case, we want the credit manager’s approval 
for the credit limit change, and we are sending the request to the manager’s external e-mail address. 
If the credit manager approves the change, the system writes and saves it. If the credit manager does 
not approve the change, the system rolls back the record to the previously approved credit limit. 
As with the other scenarios so far, we can use existing framework events and IDOs to accomplish 
this. This time, however, because we are sending out a prompt and requiring a response from the 
credit manager, we must make it a synchronous and suspending event handler. 
This event handler requires three actions: 
z
One checks whether the Credit Limit field has been changed. If it has not, it finishes with a status 
of Success. 
z
One sends the prompt message and external e-mail. 
z
If the credit manager does not approve the change, the third one fails the event and rolls back the 
record. 
To accomplish this scenario: 
1.
Set up the recipient in the Users form to allow external e-mail and to have the appropriate default 
language code.
z
Select Send E-mail Prompts
z
Ensure that the E-mail Address is correct
z
Specify the Default Language to use for formatting text strings
2.
Create an event handler with these settings: 
z
Event Name = IdoOnItemUpdate

z
Applies to Objects = SLCustomers 
3.
Save the handler. 
4.
Create the first action, which checks the condition of the Credit Limit field when the customer 
record is saved: 
a.
Click Event Actions for the handler you just created. 
b.
In the Event Actions form, create a new action with these settings: 
z
Action Sequence = 10 
z
Action Type = Finish 
c.
Click Edit Parameters. 
d.
Starting with the Event Action Finish form, use the associated forms to create these 
parameters:  
e.
Verify that the syntax is correct. 
f.
Save the action. 
5.
Create the second action, to send the prompt message. 
Note: If you still have the handler you created for “Notification of Changes to an 
Existing Record—Changing the Credit Limit” active, it is a good idea to clear the 
Active check box or mark it as Obsolete, so that this event handler and that one do 
not create duplicate and possibly confusing messages. 
Field / Button 
Action 
Result / Comments 
Condition button
Click. 
The Event Action Parameter Condition form 
opens. 
Expression 1 
button 
Click. 
The Event Action Expression Editor opens. 
Select a function 
Select 
PROPERTYMODIFIED. 
The system displays the Argument 1 button 
and field. 
Argument 1 field 
Specify: CreditLimit 
Then click OK. 
The system returns the expression to the 
parent Event Action Parameter Condition 
form and disables the Operator and 
Expression 2 options. 
NOT check box 
Select. 
Then click OK. 
This tells the action to finish with a status of 
Success if the Credit Limit field has not been 
changed. 
The system returns the expression to the 
Event Action Finish form. 
OK button 
Click. 
The system returns the entire parameter to 
the Event Actions form, correctly formatted.

This action sends the prompt to the credit manager, through both the Inbox form and external e-
mail, and suspends the handler until the credit manager responds to the request. 
a.
In the Event Actions form, create a new action with these settings: 
z
Action Sequence = 20 
z
Action Type = Prompt 
b.
Click Edit Parameters. 
c.
Starting with the Event Action Prompt form, use the associated forms to create these 
parameters:   
Field / Button 
Action 
Result / Comments 
To button 
Click. 
The Event Action Parameter Recipients 
form opens. 
Recipients button 
Click. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select GC. 
The system displays the Argument 1 button 
and field. 
Argument 1 drop-
down list 
Select CreditMgr. 
Then click OK. 
The system returns the expression to the 
Event Action Parameter Recipients form. 
OK button 
Click. 
The system returns the expression to the 
Event Action Prompt form. 
Subject button 
Click. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select SUBSTITUTE. 
The system displays the buttons and fields 
associated with the SUBSTITUTE function. 
Argument 1 field 
Specify: Credit limit 
change request for 
customer ID: {0} 
Notice that the SUBSTITUTE function is being 
used to present the customer’s ID number in 
the Subject line, so that messages can be 
saved and tracked more easily. 
Arguments grid, 
row 1 
Place the cursor in the field 
and then click Build 
Expression. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select P or PROPERTY. 
Note: These are equivalent 
functions. 
The system displays the Argument 1 button 
and field. 
Argument 1 drop-
down list 
Select CustNum. 
Then click OK. 
The system returns the expression to the 
parent Event Action Expression Editor 
form. 
OK button 
Click. 
The system returns the entire expression to 
the Event Action Prompt form.

Category field
Specify: Financial
— 
Body button 
Click. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select SUBSTITUTE. 
The system displays the buttons and fields 
associated with the SUBSTITUTE function. 
Argument 1 field 
Specify: You have a 
request for a credit limit 
change to ${0} for {1}, 
Customer ID {2}. Please 
respond to the question 
and indicate your approval 
on the Response tab. 
This sets up the basic message with three 
replacement markers. 
Arguments grid, 
row 1 
Place the cursor in the field 
and then click Build 
Expression. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select P. 
The system displays the Argument 1 button 
and field. 
Argument 1 drop-
down list 
Select CreditLimit. 
Then click OK. 
The system returns the expression to the first 
row of Arguments grid on the parent Event 
Action Expression Editor form. 
Arguments grid, 
row 2 
Place the cursor in the field 
and then click Build 
Expression. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select P. 
The system displays the Argument 1 button 
and field. 
Argument 1 drop-
down list 
Select Name. 
Then click OK. 
The system returns the expression to the 
second row of Arguments grid on the parent 
Event Action Expression Editor form.
Arguments grid, 
row 3 
Place the cursor in the field 
and then click Build 
Expression. 
The Event Action Expression Editor form 
opens. 
Select a function 
Select P. 
The system displays the Argument 1 button 
and field. 
Argument 1 drop-
down list 
Select CustNum. 
Then click OK. 
The system returns the expression to the third 
row of Arguments grid on the parent Event 
Action Expression Editor form. 
OK button 
Click. 
The system returns the entire SUBSTITUTE 
expression to the Event Action Prompt form. 
Field / Button 
Action 
Result / Comments

d.
Verify that the syntax is correct. 
e.
Save the action. 
6.
Create the third action, which tells the system how to respond if approval is not granted. 
This parameters tells the system to consider the action as having failed if the credit manager 
rejects the credit limit change. In other words, if the credit manager votes "No" [0] on the second 
action (Action Sequence = 20), then this action fails. 
a.
In the Event Actions form, create a new action with these settings: 
z
Action Sequence = 30 
z
Action Type = Fail 
This action type ends handler execution with an error status. This effectively aborts the 
process and prevents the credit limit from being changed for the customer. 
Question field 
Specify: Do you approve 
this credit limit change? 
Note that you have an 80-character limit in the 
Question field. 
Choices button 
Click. 
The Event Action Prompt Choices form 
opens. 
Return Value, 
row 1
Specify 1. 
Tip: Theoretically, you can use any value you 
want here, as long as you remember what it is 
and use the same value later in the Fail action 
step. 
Button Caption, 
row 1
Specify sYes. 
Notice that this is a translatable string from the 
Strings table. Also notice that you can select a 
string from the Strings table from the drop-
down list. 
Return Value, 
row 2
Specify 0. 
— 
Button Caption, 
row 2
Specify sNo. 
— 
OK button. 
Click. 
The system returns the Choices values to the 
Event Action Prompt form. 
Save in Sent 
Items 
Select. 
This sends a copy of the message to 
whomever initiated the credit limit change. 
OK button 
Click. 
The system returns the entire set of Prompt 
action parameters to the Event Actions form. 
Note: You could incorporate other field values from the Event Action Prompt 
form before saving and closing, but in the interest of relative brevity, we will finish 
with what we have here. 
Field / Button 
Action 
Result / Comments

b.
Click Edit Parameters. 
c.
Starting with the Event Action Fail form, use the associated forms to create these 
parameters:  
d.
Verify that there are no syntax errors. 
e.
Save the action and close the Event Actions form. 
7.
Return to the Event Handlers form and select the Suspend check box. 
Field / Button 
Action 
Result / Comments 
Condition button
Click. 
The Event Action Parameter Condition form 
opens. 
Expression 1 
button 
Click. 
The Event Action Expression Editor opens. 
Select a function 
Select VOTINGRESULT. 
The system displays the Action drop-down 
list field. 
Action drop-down 
list 
Select 20 Prompt. 
Notice that the system displays only the 20 in 
the field. The action type name in the drop-
down list is there to help you select the correct 
action step. 
OK button 
Click. 
The system returns the expression to the 
Event Action Parameter Condition form. 
Operator drop-
down list 
Select = (Equals). 
— 
Expression 2 field 
Specify 0 (zero). 
NOTE: This is a reference to the value you 
designated for a disapproval (sNo). If you had 
used some value other than 0, that is what 
you would specify here. 
OK button 
Click. 
The system returns the expression to the 
Event Action Fail form. 
Result field 
Specify: The credit 
manager has disapproved 
the credit limit change. 
This is the text that appears in the Result field 
of the Event Status form if the credit manager 
disapproves the change. Since that is the only 
time and place this message is displayed, you 
can use a literal value. To make it clearer, you 
could (and probably should) use a 
SUBSTITUTE function with the customer 
name and ID number. 
Note: You could also at this point set another event action to notify the original 
sender by message that the change has been approved or disapproved, but that 
is beyond the scope for this exercise.

8.
Save the handler. 
9.
Discard the cached metadata. 
For more information, including the procedure, see Refreshing the metadata cache on page 50. 
Testing this event handler 
To test this handler: 
1.
Open the Customers form and change the credit limit for a customer. Save it. 
Notice that the entire record for this customer is now temporarily disabled, because the update 
has been suspended pending approval. Therefore, no further changes can be made to this 
customer record until this event is resolved one way or the other. 
Also notice that, at this point, all fields, including the Credit Limit field, display their original 
values. Anyone (including you) who views this suspended record sees the original values, until 
this suspended event finishes successfully, at which time the new values are saved in the 
database and displayed on the Customers form. 
2.
(Optional) Open the Saved Messages form for your current logon ID and verify that a copy of the 
message has been saved there. 
3.
Open the Inbox form for the individual designated as the credit manager and verify that the 
message was received and that the Response tab displays the question and choice buttons. 
4.
Open the credit manager’s external e-mail systemand verify that the e-mail was received, and the 
question and choice links display. 
5.
(Optional) With the Customers form open and customer record that was changed selected, from 
the Actions menu, select View Event Status. 
This opens the Event Status form. Verify that the status for this event is Running. You can also 
open the Event Status form manually. 
6.
In the credit manager’s e-mail, click the link labeled Yes. Verify that the ASP processes the 
message and returns a success response. 
7.
In the credit manager’s Inbox form, verify that the message is automatically marked as Expired, 
the Choices buttons are now disabled, and the Selected Choice is Yes. 
8.
Refresh the collection on the Customers form and verify that the new credit limit was saved. 
Notice too that the entire customer record is once again enabled for editing. 
You can also do a second test, clicking the link labeled No to reject the request. In this case, when 
you refresh the Customers form, notice that the Credit Limit field has retained its original amount. 
Points to note and remember 
In creating this kind of event handler, keep these points in mind:

z
You can use the SUBSTITUTE function other places than just in the body of a message. You can 
use it in the Subject line and other places. And, as we will see later, you can also use it for 
purposes other than replacing text in messages. 
z
When checking on a voting result, the number referred to in the syntax is the action sequence 
number for the action that contains the choice. 
Extra challenges 
z
Change the body of the message to include both the original credit limit and the proposed new 
limit. 
Hint: You will need to save the old credit limit in an event variable. 
z
Create another event action to notify the original sender by message that the change has been 
approved or disapproved. 
Scenario 6: Requesting multiple and complex approvals 
In this scenario, when a purchase order (PO) status is changed to Ordered, it requires the approval 
of the purchasing manager. At the same time, if the PO is for more than $100, 000, the PO also 
requires the approval of the purchasing manager’s supervisor. Finally, if the PO is for more than 
$1,000,000, the PO requires the further approval of two senior executives. 
If the PO is disapproved at any level, the PO is rolled back to the previous values, and any changes 
made to it are lost. While it is in the process of being approved, the PO remains suspended until 
approval or disapproval is determined. This means, among other things, that if one or more approvers 
fail to respond to the request, the PO is locked and cannot be changed until all required approvers 
respond.

This flow diagram illustrates what must happen with this handler: 
For this scenario we will: 
z
Use the same global constant for the purchasing manager (PurchasingMgr) that we used for a 
previous scenario (Scenario 4: Approval for a New Record). 
z
Use the IdoOnItemUpdate framework event for the SLPos IDO. This will cause the event to be 
generated whenever a PO record is updated either in the Purchase Orders form or by another 
process that attempts to update that record. 
z
Pass property values and an identifying property (ItemId) to the event as input parameters so the 
system can store them with the event as event parameters. 
To accomplish this scenario: 
1.
Create and save an event handler with these settings: 
z
Event Name = IdoOnItemUpdate 
z
Applies to Objects = SLPos

2.
Create the require event global constants to make this scenario work. In the Event Global 
Constants form, create these global constants:  
Value for POApprovalPrompt: 
SUBJECT(" Purchase Order Update Approval Needed") 
CATEGORY("Order Approval")
TO(GC(TV(Approver))) 
Name 
Value 
Comments 
PurchasingMgr 
userID1 
This is the logon user ID for the 
purchasing manager required for initial 
approval. 
This can be the same as the one we 
created for Scenario 4: Approval for a 
New Record. 
If you have multiple recipients, separate 
them with semi-colons (;) and no 
spaces. 
PurchasingSuper 
userID2 
This is the logon user ID for the 
purchasing supervisor required to 
approve POs over $100,000. 
PurchasingSenior 
userID3;userID4 
These are the logon user IDs for the 
two senior executives required to 
approve POs over $1,000,000. 
SuperCost 

This global constant represents the 
minimum amount that must be 
approved by a supervisor. We are using 
a global constant for it so that it can be 
changed globally at some future time. 
The value is a literal amount, no 
commas. 
SeniorCost 

This global constant represents the 
minimum amount that must be 
approved by two senior-level 
executives. We are using a global 
constant for it so that it can be changed 
globally at some future time. 
The value is a literal amount, no 
commas. 
POApprovalPrompt 
[See below.] 
Note that, because we want to use the 
same basic prompt for all levels of 
approvals, we are putting it into a global 
constant. This is accomplished with the 
use of a few variables.

BODY(SUBSTITUTE("A purchase order, {0}, has been updated to Ordered status for vendor, 
{1}, number: {2}. Please review the details on the Variables tab and then indicate your 
approval on the Response tab.", 
FP("PoNum"), 
P("VendorName"), 
FP("VendNum"))) 
QUESTION("Do you approve this PO change?") 
CHOICES("1, sYes, 0, sNo")TV(CountMethod) 
FILTERFORM("PurchaseOrders") 
FILTER( SUBSTITUTE("PoNum={0}", FP("PoNum"))) 
3.
Using the Event Actions form, add the first event action: 
z
Action Sequence = 1 
z
Action Type = Finish 
a.
Starting with the Edit Parameters button, use the event action parameter forms to complete 
the event action:  
Field / Button 
Action 
Result / Comments 
Condition button
Click. 
The Event Action Parameter 
Condition form opens. 
Expression 1 
button 
Click. 
The Event Action Expression Editor 
opens. 
Select a function 
Select 
PROPERTYMODIFIED. 
The system displays the Argument 1 
button and field. 
Argument 1 field 
Specify Stat. 
— 
OK button 
Click. 
The system returns the expression to 
the Event Action Parameter 
Condition form. 
NOT check box 
Select. 
—

b.
Check the syntax and save the action. 
4.
Add the second event action: 
z
Action Sequence = 2 
z
Action Type = Set Values 
a.
Starting with the Edit Parameters button, use the event action parameter forms to complete 
the event action:  
Condition field 
Add this text: 
OR P("Stat") <> "O" 
Note: The reason this is required is that 
the Event Action Parameter 
Condition form can only be used to 
construct simple condition statements. 
For complex conditions, you can start 
with that form, but you must then 
manually edit the condition statement. 
The "O" in this case is the capital letter, 
not a zero. 
The final result of this condition is: If the 
Stat property has not been modified, or 
if the value of the Stat field is not O, 
then finish. Or, in other words, if the Stat 
property has been modified and the 
value of the field is O, then continue to 
the next action. 
OK button 
Click. 
The system returns the expression to 
the Event Action Finish form. 
Field / Button 
Action 
Result / Comments 
Variables button 
Click. 
The Event Action Set Name/Value Pairs 
form opens. 
Variable Name 
column, row 1 
Specify: Approver 
— 
Value column, 
row 1 
Click Build Expression. 
The Event Action Expression Editor opens. 
Select a function 
drop-down list 
Select GC. 
The form displays the Argument 1 button 
and drop-down list. 
Argument 1 drop-
down list 
Select PurchasingMgr and 
then click OK. 
The system returns to the Event Action Set 
Name/Value Pairs form. 
Variable Name 
column, row 2 
Specify: CountMethod 
— 
Value column, 
row 2 
Specify: 
VOTINGRULE(Plurality) 
Although this looks like a function, the system 
in this case does not treat VOTINGRULE() 
like the other functions. 
Field / Button 
Action 
Result / Comments

This action step sets the values of two variables as follows: 
z
The variable named Approver is set to the value of the global constant, PurchasingMgr, 
which is the user ID for the purchasing manager. 
z
The variable named CountMethod is set to count the votes using the Plurality rule, which 
simply says that the choice with the greatest number of votes wins. Since we have only 
one individual set to vote at this point, the purchasing manager’s vote alone determines 
what happens next. 
b.
Check the syntax and save the action. 
5.
Add the third event action: 
z
Action Sequence = 3 
z
Action Type = Prompt 
a.
In the Parameters text input field, specify this: 
TGC(POApprovalPrompt)  
This statement performs a text evaluation of the POApprovalPrompt global constant to obtain 
the parameters for a prompt action. Part of this text evaluation includes an evaluation and 
insertion of the values for the two variables we set in the previous step. 
After evaluating the POApprovalPrompt global constant, this action also sends out the prompt 
message to the purchasing manager and suspends the handler pending the manager’s 
response. Because we did not specify any Variable Access rules, the message allows the 
purchasing manager to modify any variable values before approving it. 
b.
Save the action. 
6.
Add the fourth event action: 
z
Action Sequence = 4 
z
Action Type = Branch 
OK button. 
Click. 
The system returns to the Event Action Set 
Values form. 
OK button. 
Click. 
The system returns the parameters to the 
Event Actions form, correctly formatted. 
Note: If you have more than one user ID in the PurchasingMgr global constant, 
you might want to use a different voting rule. For more information about voting 
rules, see “Voting rules” on page 62. 
Note: Because TGC( ) is a pre-parser function, you cannot use the event action 
parameter forms to create or set it. You must specify this statement directly in the 
Parameters field of the Event Actions form. This also means that you cannot 
use the Check Syntax button to check the syntax. 
Field / Button 
Action 
Result / Comments

a.
Starting with the Edit Parameters button, use the event action parameter forms to complete 
the event action:  
This action step evaluates the purchasing manager’s response (from action Sequence 3) and 
directs the handler to the next action depending on that response. If the manager approves 
the request, the handler continues to the next action. If the manager rejects the request, the 
system goes to the destination, action Sequence 14, and continues from there. 
b.
Check the syntax and save the action. 
7.
Add the next event action: 
z
Action Sequence = 5 
z
Action Type = Finish 
Starting with the Edit Parameters button, use the event action parameter forms to complete the 
event action:  
Field / Button 
Action 
Result / Comments 
Condition button 
Click. 
The Event Action Parameter Condition 
form opens. 
Expression 1 
button 
Click. 
The Event Action Expression Editor opens. 
Select a function 
drop-down list 
Select VOTINGRESULT. 
The Action drop-down list appears. 
Action drop-down 
list 
Select 3 Prompt. 
The Action field displays 3. 
OK button 
Click. 
The system returns to the Event Action 
Parameter Condition form. 
Operator drop-
down list 
Select <>. 
— 
Expression 2 
field 
Specify: 1 
— 
OK button 
Click. 
The system returns to the Event Action 
Branch form. 
Destination drop-
down list 
Specify: 14 
Even though we have not yet created action 
Sequence 14, we can specify the number 
here. This is the action to which we will 
eventually be jumping if the purchasing 
manager rejects the request. 
OK button 
Click. 
The system returns the action parameters to 
the Event Actions form, correctly formatted. 
Field / Button 
Action 
Result / Comments 
Condition button 
Click. 
The Event Action Parameter Condition 
form opens. 
Expression 1 
button 
Click. 
The Event Action Expression Editor opens.

This action step determines whether the cost of the PO is less than $100,000, the value of the 
SuperCost global constant. If it is, then the handler commits the PO record to the database, 
writes the result to the event state (viewable on the Event States form), and finishes with a 
status of Success. If the PO cost is $100,000 or greater, then the handler continues to the 
next action. 
8.
Add the next event action: 
z
Action Sequence = 6 
z
Action Type = Set Values 
This action step is similar to action Sequence 2, the difference being: 
z
The variable named Approver is set to the value of the global constant, PurchasingSuper, 
which is the user ID for the purchasing manager’s supervisor. 
z
The variable named CountMethod is set to count the votes using the Majority rule, which 
says that any choice that gets more than 50% of the vote wins. If we had three supervisors 
voting, for instance, whichever choice gets the first two votes determines the outcome. Since 
we have only one individual set to vote at this point, the purchasing supervisor’s vote alone 
determines what happens next. 
9.
Add the next event action: 
z
Action Sequence = 7 
Select a function 
drop-down list 
Select P. 
The Argument 1 button and field display. 
Argument 1 field 
Specify: POCost. 
This property name is derived from the 
Purchase Orders form. 
OK button 
Click. 
The system returns the statement to the 
Event Action Parameter Condition form. 
Operator drop-
down list 
Select <. 
— 
Expression 2 
button 
Click. 
The Event Action Expression Editor opens. 
Select a function 
drop-down list 
Select GC. 
The Argument 1 button and field display. 
Argument 1 
drop-down list 
Select SuperCost. 
— 
OK button 
Click. 
The system returns the statement to the 
Event Action Parameter Condition form. 
OK button 
Click. 
The system returns the condition parameter 
to the Event Action Finish form. 
Result field 
Specify: Approved by 
Purchasing Manager. 
— 
OK button 
Click. 
The system returns to the Event Actions 
form with the parameters correctly formatted. 
Field / Button 
Action 
Result / Comments

z
Action Type = Prompt 
In the Parameters text input field, specify this: 
TGC(POApprovalPrompt) 
As in action Sequence 3, this action step performs a text evaluation of the POApprovalPrompt 
global constant to obtain the parameters for a prompt action. This time, the prompt uses the new 
variable values for the purchasing supervisor that were set in Step 8. 
After evaluating the POApprovalPrompt global constant, this action sends out the prompt 
message to the purchasing supervisor and suspends the handler again, pending the supervisor’s 
response. Again, because we did not specify any Variable Access rules, the message allows the 
purchasing supervisor to modify any variable values before approving it. 
10. Add the next event action: 
z
Action Sequence = 8 
z
Action Type = Branch 
This action is similar to action Sequence 4, with the sole difference being that for the 
VOTINGRESULT( ) expression, we look at action Sequence 7 instead of Sequence 3. 
This action, then, evaluates the purchasing supervisor’s response (from Action Sequence 7). As 
soon as any choice has a majority (more than 50% of the votes), the system directs the handler to 
the next action depending on that response. 
In this case, if the supervisor approves the request, the handler continues to the next action. If the 
supervisor rejects the request, the system goes to the destination, action Sequence 14, and 
continues from there. 
11. Add the next event action: 
z
Action Sequence = 9 
z
Action Type = Finish 
This action is similar to action Sequence 5, with these differences: 
z
The global constant to use for the condition expression is SeniorCost, instead of SuperCost. 
z
The Result statement should read: Approved by both the purchasing manager and the 
purchasing supervisor. 
This action step determines whether the cost of the PO is less than $1,000,000, the value of the 
SeniorCost global constant. If it is, then the handler commits the PO record to the database, 
writes the result to the event state (viewable on the Event States form), and finishes with a status 
of Success. If the PO cost is $1,000,000 or greater, then the handler continues to the next action. 
12. Add the next event action: 
z
Action Sequence = 10 
z
Action Type = Set Values 
SETVARVALUES(Approver="PurchasingSenior", 
CountMethod="VOTINGRULE(MinimumPercentage) MINIMUM(100)") 
This action step is similar to action Sequences 2 and 6, the differences being: 
z
The variable Approver is set to the value of the global constant, PurchasingSenior, which is 
the user IDs for the senior-level executives who must approve requests over $1,000,000.

z
The variable named CountMethod is set to count the votes using the MinimumPercentage 
rule, which says that the first choice to reach a minimum percentage determines the next 
action. In this case, the minimum percentage is 100%, so all recipients must approve for the 
PO to reach final approval. If any recipient rejects the request, the entire request is rejected, 
no matter who has approved it to that point. 
TIP: The MinimumPercentage voting rule requires that you specify a minimum percentage 
for passage. This means that, in addition to the VOTINGRULE( ) keyword, you must also 
specify the MINIMUM( ) keyword as part of the variable definition. The resulting declaration 
for the Value column of the CountMethod variable is: VOTINGRULE(MinimumPercentage) 
MINIMUM(100) 
13. Add the next event action: 
z
Action Sequence = 11 
z
Action Type = Prompt 
In the Parameters text input field, specify this: 
TGC(POApprovalPrompt) 
As in action Sequences 3 and 7, this action step performs a text evaluation of the 
POApprovalPrompt global constant to obtain the parameters for a prompt action. This time, the 
prompt uses the new variable values for the senior-level executives that were set in the previous 
step. 
After evaluating the POApprovalPrompt global constant, this action sends out the prompt 
message to the senior executives. Again, because we did not specify any Variable Access rules, 
the message allows the executives to modify any variable values before approving it. 
14. Add the next event action: 
z
Action Sequence = 12 
z
Action Type = Branch 
This action is similar to action Sequences 4 and 8, with the difference being that for the 
VOTINGRESULT( ) expression, we look at action Sequence 11. 
This action step evaluates the senior executives’ responses (from action Sequence 11). If both 
executives vote to approve the request, then the handler moves on to the next action. If either or 
both of them vote to reject the request, then the handler goes to the destination, action Sequence 
14, and continues from there. 
15. Add the next event action: 
z
Action Sequence = 13 
z
Action Type = Finish 
a.
In the Event Action Finish form (reached by clicking Edit Parameters), in the Result field, 
specify: Purchase order change approved by senior purchasing executives. 
This action sequence commits the PO record to the database, writes the result to the event 
state (viewable on the Event States form), and finishes with a status of Success. 
b.
Save all actions. 
16. Add the next event action: 
z
Action Sequence = 14

z
Action Type = Notify 
For any result which ends up in a disapproval of the request change, this action step sends a 
notification message to the individual who made the original change to the PO status, letting that 
individual know that the change request has been disapproved at some level. 
a.
Use the event action parameter forms to create this notification message event action: 
TO(ORIGINATOR()) 
SUBJECT(SUBSTITUTE("Purchase order {0} change request disapproved", 
FP("PoNum"))) 
CATEGORY("Notification")
BODY(SUBSTITUTE("Your purchase order change request for PO {0} for {1}, vendor number: 
{2} has been disapproved. If you have questions, please see the required approvers.", 
FP("PoNum"), 
P("VendorName") , 
FP("VendNum"))) 
SAVEMESSAGE(FALSE) 
b.
Check the syntax and save the action. 
17. Add the final event action: 
z
Action Sequence = 15 
z
Action Type = Fail 
In the Event Action Fail form, set the Result field to: 
PO change not approved. 
This action step writes the result of the rejection to the event state (viewable on the Event States 
form), and exits with a status of Failure. 
18. Now that all event actions (including the requisite adjourning actions) have been created and 
saved, go back to the Event Handlers form and select the Suspend check box. 
19. Save the handler. 
20. (Optional) Click the Diagram button to view the diagrammatic view of the event handler flow in 
the Event Handler Diagram form. 
21. Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Test 1 for this handler 
In the first test, create a purchase order for less than $100,000 and let the Purchasing Manager 
disapprove it. 
Expected result: The PO status is not changed to Ordered. 
To perform this test: 
1.
On the Purchase Orders form create a new PO and save it. 
2.
On the Purchase Order Lines form, create a line for an amount of less than $100,000.

3.
On the Purchase Orders form, change the status for the line you just created to Ordered and 
save the PO. 
Notice that the PO record is disabled because it is now in a suspended state. The status appears 
to revert to Planned, because it has not yet been approved and thus, it has not yet actually been 
changed in the database. 
4.
Logged in using the Purchasing Manager’s user ID, open the Inbox form. 
5.
Read the new prompt message that the system generated, and on the Response tab, select the 
No option. 
6.
Open or refresh the Purchase Orders form, and verify that the new PO line status is still Planned 
and that the PO is again enabled for changes. 
Test 2 for this handler 
This is the same as Test 1, except this time have the purchasing manager approve the change. Verify 
that the status is changed to Ordered and the PO is again enabled for change. 
Test 3 for this handler 
Create a PO with a total cost of between $100,000 and $1,000,000. Have the purchasing supervisor 
disapprove and verify that the change is rolled back. 
Test 4 for this handler 
Do the same as Test 3, except have both the purchasing manager and purchasing supervisor 
approve the change. Verify that the change is written to the database and that the record is again 
enabled for other changes. 
Additional tests 
For complete thoroughness, other tests could (and should) be devised and conducted before making 
this event handler live on an active system. 
For example, you could change the status to something other than Ordered and make sure that the 
PO change does not suspend. You should also test for the senior executive approvals and 
disapprovals. 
Points to note and remember 
z
Whenever possible, use the event action parameter forms (accessible by way of the Edit 
Parameters button). This is your best insurance against syntax errors.

z
Not all actions can be created using the event action parameter forms. This is particularly true of 
the pre-parser functions. In these cases, you cannot check the syntax for these actions using the 
Check Syntax button. 
z
You can create whole actions using global constants. You cannot subsequently check these for 
syntax errors, though, using the Check Syntax button, so proceed with caution. 
Extra challenges 
z
Add the user ID to the Result statements for both approvals and disapprovals. 
z
Have the system generate a message to the user who initiated the request notifying that user that 
the request has been approved. 
Modifying records 
Scenario 7: Adding information to a record 
In this scenario, we want to notify a credit manager that a new customer is being added and ask the 
credit manager to determine what the credit limit will be for that customer. So, we must send a 
notification that prompts the credit manager for a response and then uses the data from that response 
to add data to the pending new customer record and commit the changes to the database. 
For this scenario we will: 
z
Use the same global constant (CreditMgr) we used for previous scenarios. 
z
Use the IdoOnItemInsert framework event. 
To accomplish this scenario: 
1.
Create and save the event handler with these settings: 
z
Event Name = IdoOnItemInsert 
z
Applies to Objects = SLCustomers 
2.
Create one action, which sends a prompt to the credit manager requesting a response: 
z
Action Sequence = 10 
z
Action Type = Prompt 
a.
Use the Event Action Prompt form and associated event action parameter forms to create 
these parameters: 
z
TO = GC(CreditMgr) 
z
SUBJECT = SUBSTITUTE("Need credit limit for customer ID {0}, {1}", 
FP("CustNum"), P("Name")) 
z
CATEGORY = "Financial" 
z
BODY = SUBSTITUTE("Please use the Variables tab to provide a credit limit for 
customer ID {0}, {1}. Then use the Post button on the Response tab to register the 
new credit limit.", FP("CustNum"), P("Name") )

z
SAVEMESSAGE = FALSE 
z
QUESTION = To post the credit limit, click the button below. 
z
CHOICES = 1,sPost 
z
FILTERFORM = Customers 
z
FILTER = SUBSTITUTE("CustNum={0}", FP("CustNum")) 
b.
On the Variable Access tab: 
z
Name = CreditLimit 
z
Access = Mandatory 
This forces a response from the credit manager. 
c.
Save the action and close the Event Actions form. 
3.
Return to the Event Handlers form and select the Suspend check box. 
4.
Save the handler. 
5.
Discard the cached metadata. 
For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Testing the event handler 
1.
Open the Customers form and create a new customer record. Save it. 
Notice that the newly saved record does not appear in the list of customers at this point when you 
refresh the Customers form. 
2.
Using the credit manager’s logon, open the credit manager’s Inbox. 
The new message should appear in the Inbox. 
3.
On the Variables tab, locate the Row.CreditLimit variable and specify an amount. 
4.
Save the record. 
5.
On the Response tab, click Post. 
6.
Back on the Customers form, refresh the form and verify that the newly created record appears 
in the list. 
You can (and should) also devise other test to verify that the system behaves as expected when the 
credit manager posts the response without specifying a value in the Row.CreditLimit variable field. 
Points to note and remember 
When creating a handler like this one, keep these points in mind: 
z
Because the variables are listed on the Variables tab and the question and response buttons are 
on the Response tab of the message, you should design your message body to include brief but 
detailed instructions for responding to the request. Do not assume the recipient will know or 
remember.

z
Because we did not specify variable access rules to address property variables other than the 
CreditLimit variable, all the variable property values associated with the Customers form are 
displayed and writable. That means that the credit manager, if desired, can change any variable 
data before saving the data and posting it to the database by clicking Post. (To make other 
variables non-writable, you must set the variable access for each individually.) 
z
The fact that the prompt message was sent to a single recipient (in this case) means that only one 
vote is required for a quorum, and once the credit manager posts the response, the vote is final 
and the database is updated. If there are multiple recipients associated with the CreditMgr global 
constant, then you might also need to set voting rules to determine how the responses will be 
handled. In this case, it is not necessary, because the system assumes a Plurality voting rule, and 
with only one recipient, that means that the first to respond is the one whose data is committed. 
z
If the credit manager never votes, the record is never committed to the database, but it remains 
adjourned indefinitely. 
z
The QUESTION parameter has a limit of 80 characters. 
Voting
Scenario 8: Voting for various choices
In this scenario, we need several managers at the same level to approve an engineering change, by 
means of a response to a message. So, we must send a notification that prompts the managers for a 
response. If at least two of the managers send responses approving the change, we then approve the 
requested change in the application. 
For this scenario we will: 
z
Assume that global constants were created for EngineeringMgr, ProjectMgr, and ProgramMgr. 
The creation of global constants is described in previous scenarios. 
z
Use the IdoOnItemUpdate framework event. 
To accomplish this scenario: 
1.
Create and save the event handler with these settings: 
z
Event Name = IdoOnItemUpdate 
z
Applies to Objects = SLECNs 
z
Description = ECN Approval 
2.
Create one action, which sends a prompt to the managers requesting a response: 
z
Action Sequence = 10 
z
Action Type = Prompt 
a.
Use the Event Action Prompt form and associated event action parameter forms to create 
these parameters: 
z
TO = GC(EngineeringMgr) + ';' +GC(ProjectMgr) + ';' +GC(ProgramMgr) 
z
SUBJECT = SUBSTITUTE("Need approval for engineering change {0}, {1}", 
P("EcnNum"), P("ReasonCodeDescription"))

z
CATEGORY = "Engineering" 
z
BODY = "Please review the proposed engineering change on the Variables tab. 
Then use the Approve or Reject buttons on the Response tab to register your 
response. " 
z
SAVEMESSAGE = FALSE 
z
QUESTION = To approve or reject, click the buttons below. 
z
CHOICES = 1,sApprove, 0,sReject 
z
VOTINGRULE = Minimum Count Preferred Choice 
z
PREFERREDCHOICE = 1 
z
MINIMUM = 2 
z
FILTERFORM = EngineeringChangeNotices 
z
FILTER = SUBSTITUTE("ECNNum={0}", FP("ECNNum")) 
c.
Save the action. 
If you have done everything correctly, your syntax for this action step should look like this: 
TO('' + GC(EngineeringMgr) + ';' + GC(ProjectMgr) + ';' + GC(ProgramMgr))
CATEGORY("Engineering")
SUBJECT(SUBSTITUTE("Need approval for engineering change {0}, {1}", P("EcnNum"), 
P("ReasonCodeDescription")))
BODY("Please review the proposed engineering change on the Variables tab. Then use 
the Approve or Reject buttons on the Response tab to register your response.")
SAVEMESSAGE(FALSE)
QUESTION("To approve or reject, click the buttons below.")
CHOICES("1,sApprove,0,sReject")
VOTINGRULE(MinimumCountPreferredChoice)
MINIMUM(2)
PREFCHOICE("1")
FILTERFORM("EngineeringChangeNotices")
FILTER(SUBSTITUTE("ECNNum={0}", FP("ECNNum"))) 
3.
Create the second action, which tells the system how to respond if approval is not granted: 
z
Action Sequence = 20 
z
Action Type = Fail 
This action type ends handler execution with an error status. This effectively aborts the 
process and prevents the ECN from being changed in the database. 
a.
Starting with the Event Action Fail form, use the associated forms to create these 
parameters: 
z
CONDITION(VOTINGRESULT(10) = "0") 
z
RESULT("The ECN change request was rejected by the managers.") 
b.
Save the action and close the Event Actions form. 
4.
Return to the Event Handlers form and select the Suspend check box. 
5.
Save the handler. 
6.
Discard the cached metadata.

For more information, including the procedure, see “Refreshing the metadata cache” on page 50. 
Testing the event handler 
To test this handler: 
1.
Open the Engineering Change Notices form and update an existing ECN. Save it. After you 
save the ECN, when the Engineering Change Notices refreshes the display, the record should 
be disabled for updating. It remains read-only until/unless it has been approved. 
2.
(Optional) With the Engineering Change Notices form selected, from the Actions menu, select 
View Event Status. This opens the Event Status form. Navigate to the last row and verify that 
the status for this event is Running. 
3.
Open the Inbox form for the individual designated as the Engineering Manager and verify that the 
message was received and that the Response tab displays the question and choice buttons. 
Click the button labeled Yes. 
4.
Open the Inbox form for the individual designated as the Project Manager and verify that the 
message was received and that the Response tab displays the question and choice buttons. 
Click the button labeled Yes. 
5.
Refresh the collection on the Engineering Change Notices form and verify that the ECN now 
displays normally (read/write) and shows your changes. As soon as two managers vote for the 
preferred choice, voting is closed and the change is approved. The third manager's vote is not 
needed. 
You can also do a second test, clicking the button labeled No to reject the request by all three 
managers. In this case, when you refresh the Engineering Change Notices form, the ECN record 
displays normally but your changes are gone. 
Points to note and remember 
When creating this kind of event handler, keep these points in mind: 
z
When creating a message that requires a response from the recipient (usually a Prompt action 
type), you must mark the handler so that it suspends when executed. This means that it is also 
automatically marked as a synchronous handler. 
z
Because these event handlers must be suspended, pending the managers' responses, the 
Framework Event Service must be enabled for the configuration in which you are logged on. 
Localizing message contents 
Scenario 9: Translating captions in a purchase request 
This scenario uses strings in captions so the text can be read by users in different countries.

Metadata setup 
These strings must exist in the Forms database Strings tables: 
Event message category 
In the Event Message Categories form, set up the Category FORMAT(sOrder Approval), with the 
description Approval of an Order. 
Event action parameters 
Create an event action that includes these parameters: 
After the event action execution, the full components of the message in the database are: 
Strings.Name 
Strings.String 
SpainString.String 
sItem 
Item 
Prod 
sWhse 
Whse 
Alm 
sPoitemApprovalQuestion 
Do you approve of 
purchasing %1 %2 of [%3: 
%4] for delivery to [%5: %6] 
Usted aprueba de comprar %1 
%2 del %3 "%4" para la entrega al 
%5 "%6" 
sPoitemApproval 
Purchase Approval 
Aprobación de Comprar el 
Artículo 
sOrderApproval 
Order Approval 
Aprobación del Documento 
...
QUESTION (
  CLIENTSUBSTITUTE(
    "sPoitemApprovalQuestion",
    P(QtyOrdered),
    P(UMDesc),
    "STRINGS(sItem)",
    P(Item), "STRINGS(sWhse)", 
    P(Whse)
  )
)
SUBJECT(
  CLIENTSUBSTITUTE(
    P(PoitemApproval)
  )
)
CATEGORY("FORMAT(sOrder Approval)")
...

z
EventMessage.Question 
z
FORMAT(sPoItemApprovalQuestion, ~LIT~(100.0), ~LIT~(Metric Tons), STRINGS(sItem), 
~LIT~(5" screw/x03 chrome\x04hex head\x05), STRINGS(sWhse), ~LIT~(MAIN)) 
z
EventMessage.Subject 
z
FORMAT(sPoItemApproval) 
z
EventMessage.Category 
z
FORMAT(sOrderApproval) 
Results (English)
An English-speaking user who refreshes the Inbox sees this message:  
Results (Spanish) 
A Spanish-speaking user who refreshes the Inbox sees this message:  
More advanced scenarios 
Scenario 10: Opening a session in a remote environment 
In this scenario, we want to call in to another site or another Mongoose application environment and 
return a specific discrete piece of information from the remote application database. In this scenario, 
we want to return the On Hand quantity of an item in another site. 
For the details of and procedure for this scenario, see the Integrating IDOs with External Applications 
guide. 
Component 
Text 
Question 
Do you approve of purchasing 100.0 Metric Tons of [Item: 5" 
screw, chrome (hex head)] for delivery to [Whse: MAIN] 
Subject 
Purchase Approval 
Category 
Order Approval 
Component 
Text 
Question 
Usted aprueba de comprar 100.0 Metric Tons del Prod "5" screw, 
chrome (hex head)" para la entrega al Alm "MAIN" 
Subject 
Aprobación de Comprar el Artículo 
Category 
Aprobación del Documento

Scenario 11: Cross-site event firing - adding a message to another site's 
Inbox
This scenario illustrates the general requirements used to set up cross-site event firing. Our example 
adds a message to another site’s Inbox form. 
z
An event handler called GenericNotify is available in every target site. You can fire this event to 
perform the "remote" work. 
This event has one handler with one action that performs a Notify, using event parameters for To, 
Subject, Category, and Body. 
z
A stored procedure called dbo.FireGenericNotifySp is available in every target site. You can use 
this stored procedure to fire the event. This stored procedure accepts the T-SQL parameters 
@To, @Subject, @Category and @Body, and it fires the GenericNotify event, passing in the 
information that the event needs. 
Note: You could do the same thing using a hand-coded IDO Method that calls 
Mongoose.EventSystem.EventHandlers.FireApplicationEvent(), in case the event needs to perform 
IDO-level actions.  However, for this scenario, using the stored procedure is easier. 
z
Where you want to add a message to another site's inbox, your event handler includes a Dispatch 
IDO Request action, providing these parameters:  
Parameter 
Description 
URL( ) 
URL of an IDO Request Service that serves the target site 
Sample value: 
http://MyUtilityServer/IDORequestService/RequestService.aspx 
CONFIGNAME( ) 
Name of a configuration whose application database contains the target 
site.  (Mongoose requires a configuration that is named after each site, 
so you can use the site name here.) 
Sample value: 
E(SiteId) 
IDOREQUEST( ) 
Invoke “SP!” (or the name of an IDO) plus the name of the stored 
procedure (in this case FireGenericNotifySp), passing in the event 
parameters as method parameters to the “method.” 
Sample value (shown as XML to allow pasting into the form): 
SUBSTITUTE('<RequestHeader Type="Invoke"> <InitiatorType /> 
<InitiatorName /> <SourceName /> <TargetName /> <RequestData> 
<Name>SP!</Name> <Method>FireGenericNotifySp</Method> 
<Parameters> <Parameter>{0}</Parameter> <Parameter>{1}</
Parameter> <Parameter>{2}</Parameter> <Parameter>{3}</
Parameter> <Parameter ByRef="Y" /> </Parameters> </RequestData> 
</RequestHeader>', E(ToParm), E(SubjectParm), E(CategoryParm), 
E(BodyParm))

z
If you have multiple intranets that do not serve all sites, and you want the event to fire across 
intranets, you may need to set up an event global constant for each intranet (or site) URL, and 
select one of those at runtime. 
z
The sample action shown here assumes that the originating user has the same password on the 
source and target sites, which allows it to log in for the Invoke.  If this may not be the case, you 
can instead set up a generic remote user, with permissions only to perform this one Invoke, and 
specify the USERNAME() and PASSWORD() parameters on the Dispatch IDO Request action. 
Alternatively, you can adjust the USELOCALPASSWORD() parameter. 
z
If you want to perform a different type of remote work, you can set up your own events with 
handlers and actions to address the work you want to do. Then you can create stored procedures 
to fire those events, and finally call those stored procedures using Dispatch IDO Request actions 
in the appropriate existing handlers.

### Appendix B: Reference Tables
*Pages 119-130*

B
Appendix B: Reference Tables
This appendix provides several reference tables containing detailed information about various 

z
Firing events 
z
Summary of synchronous functionality 
z
Framework events 
z
Application events 
z
Event action types 
z
Event action parameters 
z
Expressions and functions 
z
Expression operators

Firing events 
This table provides details about: 
z
Where events can be generated from (Tier) 
z
What can be used to generate them from that location (Triggered by) 
z
How to set them up (Details for construction) 
z
Whether the event is generated as a synchronous or asynchronous event (Synchronous?) 
Tier 
Triggered by 
Details for construction 
Synchronous? 
Client 
Event handler in 
form 
Use a response type of Generate 
Application Event, select the Synchronous 
option. 
Yes 
Use a response type of Generate 
Application Event, clear the Synchronous 
option. 
No 
Script in form 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, with the 
SYNCHRONOUS( ) parameter. 
Yes 
Generate a custom form event. 
Create a form event handler for that custom 
event with a response type of Generate 
Application Event, without the 
SYNCHRONOUS( ) parameter. 
No 
Middle 
Custom IDO 
method 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of True. 
Yes 
Invoke the FireApplicationEvent( ) static 
.NET method with the Synchronous 
parameter passed in with a value of False. 
No 
Database 
T-SQL 
Use the command: EXEC FireEventSp 
Yes 
Use the command: EXEC PostEventSp 
No 
Any 
An event action 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(true). 
Yes 
Use the GenerateEvent action type with a 
parameter of SYNCHRONOUS(false). 
No 
An event trigger 
Select the Synchronous option. 
Yes 
Clear the Synchronous option. 
No

Summary of synchronous functionality 
Source 
Synchronous? 
Consists of 
Requester 
Initial 
executor 
Framework 
Yes 
Synchronous (none 
marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
IDO Runtime 
IDO Runtime 
Database 
Database 
Synchronous (some 
marked Suspend) & 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
(validating 
mode) 
Event Service 
(Committing 
mode)
IDO Runtime 
FireEvent 
OR 
Generate 
Event 
with 
Synchronous
(True) 
Yes 
Synchronous and 
asynchronous event 
handlers 
WinStudio 
IDO Runtime 
IDO Runtime 
IDO Runtime 
Database 
Database 
Event service 
Event service 
PostEvent 
OR 
Generate 
Event 
with 
Synchronous
(False) 
No 
Synchronous and 
asynchronous event 
handlers 
WinStudio 
Event service 
IDO Runtime 
Database 
Event service 
Context 
Synchronous? 
Suspending?
Event’s or 
prior event 
handler’s 
executor
Initial 
executor 
Can 
adjourn? 
Suspending 
event (always 
generated 
synchronously) 
Yes 
No 
IDO Runtime 
(validating mode) 
IDO Runtime 
No 
Event service 
(committing 
mode) 
Event service
Yes 
Event service 
Event service 
Yes

Framework events 
This table lists and describes the framework (Core) events that ship with the system. You can create 
handlers that execute when these events are generated, but you cannot create your own triggers for 
these events. 
Non-
suspending 
event 
generated 
synchronously 
Yes 
n/a 
WinStudio 
IDO Runtime 
Yes 
IDO Runtime 
IDO Runtime 
Database 
Database 
Event service 
Event service
Non-
suspending 
event 
generated 
asynchronously 
Yes 
n/a 
WinStudio 
Event service 
Yes 
IDO Runtime 
Database 
Event service 
Any event 
No 
n/a
WinStudio 
Event service 
Yes 
IDO Runtime 
Database 
Event service 
Event name 
Trigger 
Context attributes passed as 
event parameters, in addition to 
the object name 
BodOnReceive 
An inbound BOD is received 
by the ION instance 
associated with the current 
site. 
BODVERB() 
BODNOUN() 
BODXML 
IdoOnLoadCollection 
An IDO collection is being 
loaded into the system. 
Load flags 
Property names 
Post query actions 
IdoPostLoadCollection 
An IDO collection has 
finished loading into the 
system 
Result set 
Context 
Synchronous? 
Suspending?
Event’s or 
prior event 
handler’s 
executor
Initial 
executor 
Can 
adjourn?

IdoOnUpdateCollection 
An update to an IDO 
collection update is being 
performed. 
Custom insert specification 
Custom update specification 
Custom delete specification 
IdoOnItemInsert 
An IDO item is being inserted 
into a collection. 
Row (IDO item) being inserted 
IdoPostItemInsert 
An IDO item has been 
inserted into a collection. 
Row (IDO item) that was inserted 
IdoOnItemUpdate 
An IDO item is being 
updated. 
Row (IDO item) being updated 
Modified flags 
IdoPostItemUpdate 
An IDO item has finished 
updating. 
Row (IDO item) that was updated 
Modified flags 
IdoOnItemDelete 
An IDO item is being deleted. 
Row (IDO item) being deleted 
IdoPostItemDelete 
An IDO item has been 
deleted. 
Row (IDO item) that was deleted 
IdoPostUpdateCollection 
All IDO collection updates 
have finished processing. 
— 
IdoOnInvoke 
An IDO method is being 
invoked. 
Name of the IDO method that was 
invoked 
Number of parameters passed to 
the method
Values of the parameters passed 
to the method
IdoPostInvoke 
An IDO method has been 
invoked. 
Name of the IDO method that was 
invoked 
Number of parameters passed to 
the method
Values of the parameters passed 
to the method
IdoOnPersistFailed 
An exception occurs during a 
create, update, or delete 
operation. 
DBErrorDataKeys (number of keys 
that exist in the DBErrorData[] 
array) 
DBErrorDataKeyList (comma-
separated list of the keys that exist 
in the DAErrorData[] array) 
SessionOnLogin 
A new session is being 
requested. 
User name 
Event name 
Trigger 
Context attributes passed as 
event parameters, in addition to 
the object name

SessionOnLoginFailed 
A login attempt has failed. 
z The application name 
z Configuration information, 
including the configuration 
name, application ID within the 
configuration, and the site to 
which the configuration belongs 
z User information, including the 
user name, password (either 
encrypted or not), domain, 
workstation info (if applicable), 
and token authentication 
passcode (if applicable) 
z The name of the computer from 
which the login attempt 
originated 
z Additional system and login 
failure information 
SessionOnLogout 
A session has been closed. 
User name 
SessionOnVarChanged 
A session variable’s value is 
being changed. 
The name and new value of the 
session variable 
SessionPostVarChanged 
A session variable’s value 
has been changed. 
The name and new value of the 
session variable 
Event name 
Trigger 
Context attributes passed as 
event parameters, in addition to 
the object name

Application events
This table lists and describes the application events that ship with the system. To use these events, 
you can employ the event handlers that already exist for these events. 
Event name 
Trigger 
Context attributes to be passed 
as event parameters, in 
addition to the object name 
GenericNotify 
z When the Task List (or 
anyone else) fires this 
event for a reminder 
z When the 
NotifyPublication-
SubscribersSp stored 
procedure is called for a 
subscriber who has no e-
mail address 
ToVar, SubjectVar, CategoryParm, 
BodyVar, HTMLBodyVar (To, 
Subject, Category, and whether 
the Body is expressed in HTML, of 
the Notify action) 
GenericNotifyWithAttach-
ments 
When someone clicks the 
“Send Email for the current 
object” button on the toolbar 
For internal use only. This event 
and its actions are specific to and 
integrated with a Core process. 
GenericSendEmail 
z When the NotifyPublica-
tionSubscribersSp stored 
procedure is called for a 
subscriber who has an e-
mail address 
z Upon receipt of a 
SyncPulseNotification or 
SyncPulseAlert BOD, if 
Process Default “ION pulse 
interface” is set to 1 
EmailTo, EmailCc, EmailSubject, 
EmailMessage, 
EmailHTMLFormat (To, Cc, 
Subject, Body, and whether the 
Body is expressed in HTML, of the 
Send Email action), 
AttachmentFileList, 
AttachmentNameList, 
AttachmentDocTypeList (lists of 
files to attach to the email, their 
names, and document types) 
GenericSendPulseAlert-
BOD 
N/A – This event is not used 
directly by the framework; it is 
available for applications to 
fire. 
UserEmail, MessageSubject, 
MessageDescription, 
MessageBody 
ProcessNewDataMaint-
enance 
When someone clicks Finish 
in the New Data 
Maintenance Wizard 
For internal use only. This event 
and its actions are specific to and 
integrated with a Core process. 
TaskListCheck 
When the TaskListCheck 
event trigger fires from the 
Event Service 
None, as there is no reason to fire 
it apart from the existing event 
trigger

Event action types 
This table lists and describes the action types available for use when defining event actions. For 
details about the associated event action parameters, including their syntax and examples, see 
“Event action parameters” on page 126. 
WinStudio includes a variety of action types for use when defining event actions. These action types 
are predefined to perform their specified actions when the required parameters are provided. 
In every case, WinStudio includes special event action forms for each event action. These forms are 
designed to help you more easily set up the required and optional parameters for their respective 
event actions. For more information, see the online help for the desired event action form. 
Note: Adjourning event action types (that is, Prompt, Wait, and Sleep) cannot be assigned to event 
actions on a transactional event handler. For more information about adjournment, see “Adjournment 
and resumption” on page 21. For more information about transactional event handlers, see 
“Transactions” on page 24. 
Note: Mid-tier event action types (that is, Call IDO Method, Dispatch IDO Request, Execute IDO 
Request, Load Collection, Load IDO Row, and Update Collection) cannot be executed on a 
synchronous event handler whose event is fired from the database layer (that is, via FireEventSp, or 
attached to any Session framework event).  If this is attempted, the handler fails with an error. 
Event action parameters 
The information formerly located in this section is now available only in the online help. See the topic 
for the parameter you are interested in or use context-sensitive help options. 
Expressions and functions 
Many event action parameters make use of multi-part expressions when performing their various 
operations. These expressions can almost always be constructed with the Event Action Expression 
Editor. which is a versatile tool that provides many options designed to help you build the parameter 
expressions you need without having to actually write code. 
To help in the construction of event action parameter expressions, WinStudio provides a large number 
of standard expression functions, which are all available in the Event Action Expression Editor. 
When selected, each function provides in the editor itself a sample of the correct syntax and a brief 
description. Many functions have more complete descriptions and examples in the online help.

Pre-parser functions 
In addition to the standard expression functions listed in the Event Action Expression Editor, there 
are two “pre-parser functions” that you can use to build expressions: 
z
TGC: Retrieves the value of an event global constant for which the value can contain other 
grammar elements. 
z
TV: Retrieves the value of an event variable in which that value can contain other grammar 
elements. 
These additional functions can be used to expand an event variable or event global constant textually, 
that is, with no assumptions about the structure or data-type of the contained value. These functions 
are useful in cases where the expanded value contains other grammar elements that must be further 
evaluated, for example, to share common expressions, expression elements, or groups of functions. 
When an event action begins, WinStudio first evaluates all TV( ) references recursively, until no more 
references to known variables remain. Next, WinStudio evaluates all TGC( ) references recursively, 
until no more references to known global constants remain. Finally, the resulting parameters string is 
passed to the parser to evaluate all other functions and operators contextually using the grammar 
found in Appendix C, Expression Grammar. 
Simple expansions 
Consider this parameters string: 
Assume that the system is using this event global constant metadata:  
The effective parameters passed to the event system parser would be: 
CONDITION(DATEDIFF(day, BEGINDATE( ), CURDATETIME( )) > 7) TO(USERNAME( )) 
SUBJECT("Old Handler Alert") QUESTION("Do you really want to continue this 
old Handler?") CHOICES("1,sYes,0,sNo") 
Complex expansions 
More complex expansions are possible. For example: 
GC(MyVarTV(VarSuffix)) 
CONDITION(TGC(Over1WeekOld)) TGC(OldHandlerPromptParms) 
Name 
Value 
Over1WeekOld 
DATEDIFF(day, BEGINDATE( ), CURDATETIME( )) > 7 
OldHandlerPromptParms 
TO(USERNAME( )) SUBJECT("Old Handler Alert") 
QUESTION("Do you really want to continue this old 
Handler?") CHOICES("1,sYes,0,sNo")

In this example, first, the value of the current event handler's "VarSuffix" variable is retrieved. Then 
that value is appended to the name "MyVar" to construct an event global constant name, for which the 
value is then retrieved. 
The value of the "VarSuffix" variable might be set dynamically by an event action on the handler, or it 
might be included in different event initial states that are linked from referring handlers, in which case 
the GC( ) reference itself could be moved to its own global constant and referred to from all actions of 
the handlers using TGC( ). 
Note that no operator or other syntax is used around the TV( ) reference, because it is evaluated and 
substituted in-place textually, without regard to data type or context. 
Nested expansions 
Nested expansions are also possible. For example, consider this parameters string: 
TGC(MarkItUp) 
Assume that the system is using this event global constant metadata:  
This has the effect of increasing the value of the "Price" variable by 10% plus 5, but only if the 
resulting value is less than 100. 
Expression operators 
Expression operators can be either unary or binary, meaning they can operate on either one or two 
expressions. Most operators are limited as to what kind of expressions they can operate with. The 
kinds of expressions possible include: 
z
Scalar expressions (scalarExpr) – These expressions can be either of a known type (numeric, 
string, or date) or an unknown type (typeless). 
In the table below, if the expression type is given as scalarExpr, it can be any of these four types. 
z
Numeric expressions (numericExpr) – These expressions evaluate using numeric values. These 
are the expressions used to perform mathematic operations. If a string or typeless expression is 
supplied where a numeric expression is expected, it is automatically converted into a numeric 
value. If that is not possible due to the presence of non-numeric characters, the current handler 
fails with an error. 
z
String expressions (stringExpr) – These expressions are text-based sets of characters. They may 
include numbers, but if so, the numbers are treated as text characters, not numerals. If another 
Name 
Value 
StdMarkup 
* 0.1 + 5 
MarkItUp 
CONDITION(V(Price)TGC(StdMarkup) < 100) 
SETVARVALUES(Price=Price TGC(StdMarkup))

type of expression is supplied where a string expression is expected, it is automatically converted 
into a string representation.
z
Date expressions (dateExpr) – These expressions involve dates or parts of dates, including times 
such as 10:00 AM. 
z
Typeless expressions (typelessExpr) – These are expressions that could be one of at least two 
different types. The way the system treats these expressions depends on the context in which the 
expression is used. 
z
Boolean expressions (BooleanExpr) – These expressions consist of an OR conjunction of one or 
more AND conjunctions. 
To construct the expressions used in “Event action parameters” on page 126, you can use the 
expression operators in this table in conjunction with the “Expressions and functions” on page 126  
Operator 
Purpose 
Example 
scalarExpr = scalarExpr 
Is equal to 
V(var) = 1 
scalarExpr != scalarExpr 
scalarExpr <> scalarExpr 
Is not equal to 
V(var) != 1 
scalarExpr > scalarExpr 
Is greater than 
V(var) > 1 
scalarExpr < scalarExpr 
Is less than 
V(var) < 1 
scalarExpr >= scalarExpr 
Is greater than or equal to 
V(var) >= 1 
scalarExpr <= scalarExpr 
Is less than or equal to 
V(var) <= 1 
scalarExpr : list 
scalarExpr IN list 
Is in the list. 
The list is enclosed in parentheses 
and the elements separated by 
semi-colons. 
V(var) IN (1;2;3;4) 
"b" : ("a";"b";"c") 
scalarExpr !: list 
Is not in the list. 
The list is enclosed in parentheses 
and the elements separated by 
semi-colons. 
V(var) !: (1;2;3;4) 
BooleanExpr AND 
BooleanExpr 
Boolean AND 
V(var) = 1 AND V(var2) > 5 
BooleanExpr OR 
BooleanExpr 
Boolean OR 
V(var) = 1 OR V(var2) > 5 
NOT BooleanExpr 
Boolean negation 
NOT(V(var) = 1 OR V(var2) 
> 5) 
numericExpr + numericExpr 
Addition 
V(var) + 1 
stringExpr + stringExpr 
String concatenation 
V(var) + "Item" 
numericExpr – numericExpr 
Subtraction 
V(var) – 1 
–numericExpr 
Unary negative 
– V(var)

For the complete grammar available for constructing expressions, see Appendix C, Expression 
Grammar. 
numericExpr * numericExpr 
Multiplication 
V(var) * 5 
numericExpr / numericExpr 
Division 
V(var) / 2 
stringExpr LIKE stringExpr 
String similarity using WinStudio 
filtering syntax: 
z The underscore ( _ ) character 
represents a single wildcard 
character. 
z The asterisk ( * ) represents any 
number of wildcard characters. 
V(var) LIKE 'A*' 
Operator 
Purpose 
Example

### Appendix C: Expression Grammar
*Pages 131-156*

C
Appendix C: Expression Grammar 
This appendix contains the complete grammar available for constructing expressions for event action 
parameters. Major sections include: 
z
Restrictions 
z
Start symbol 
z
Character sets 
z
Terminals 
z
Rules 
z
Variable, constant, and event parameter references 
z
Expressions 
z
Boolean rules 
z
Typeless rules 
z
String rules 
z
Numeric rules 
z
Date rules 
z
Restricted arguments 
z
Keyword paren lists 
z
Enumerations

Restrictions 
Expressions in this grammar are subject to these restrictions: 
z
Superfluous parentheses are usually not allowed. 
For example, this produces a parsing error: 
V(this)=1 and 2=V(that)) and 1=(2) 
Instead, you can write it like this, to work around the grammar limitation: 
V(this)=1 and 2=V(that) and 1=2 
z
Operation chains containing a mix of typed and typeless arguments must begin with a typed 
value. 
For example, this example produces an error because the first argument is not a typed value: 
'12'=V(a)+'B'+V(c) 
Instead, and because string concatenation is not commutative, you can write it as: 
'12'=''+V(a)+'B'+V(c) 
Alternatively, you can declare the type for the first argument as: 
'12'=CAST(V(a) AS STRING)+'B'+V(c) 
Again, this example produces an error because the first argument is not a typed value: 
12>V(b)+1+5 
Instead, you can write the expression in one of these ways: 
12>0+V(b)+1+5 
12>CAST(V(b) AS NUMBER)+1+5 
12>1+V(b)+5 
The last solution works because numeric addition is commutative. 
z
Functions cannot be used for variable, parameter, or constant names. 
For example, because the letter y is an abbreviation for year in the DATEPART( ) and 
DATEDIFF( ) event functions, this expression produces an error: 
y = 5 
Instead, you can declare y as yVar. This expression does not produce an error. 
yVar = 5 
Start symbol 
"Start Symbol" = <functionParenList>

Character sets 
This table lists and describes the acceptable characters for elements of the code described. You can 
include any amount of white space between elements. 
{ID Head} = {Letter} + [_] 
{ID Tail} = {Alphanumeric} + [_] + ['['] + [']'] + [.] 
{String Ch 1} = {Printable} - ["] + {LF} + {CR} 
{String Ch 2} = {Printable} - ['] + {LF} + {CR} 
Terminals 
String constants are constructed using one of these rules. The string can be: 
z
Enclosed in double-quotes, containing no double-quote characters as illustrated by this example: 
StringLiteral = "{String Ch 1}*" 
z
Enclosed in double-quotes, containing paired double-quotes that are each interpreted as a single 
embedded double-quote character as illustrated by this example: 
StringLiteral = "(""|{String Ch 1})*" 
This 
Designates 
Number 
The set of numerals: 0123456789 
Letter 
The set of all uppercase and lowercase letters: 
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ 
Alphanumeric 
The set of all characters listed as part of the Number and 
Letter sets 
Printable 
The set of all standard characters that can be printed 
onscreen. This includes the characters from  #32 to #127 and  
#160 (nonbreaking space). The nonbreaking space character 
is included because it is often used in source code. 
Whitespace 
The set of all characters that are normally considered "white 
space" and ignored by the parser. The set consists of: 
z A space (regular) 
z Horizontal  tab 
z Line feed 
z Vertical tab 
z Form feed 
z Carriage return 
z Nonbreaking space

z
Enclosed in single-quotes, containing no single-quote characters as illustrated by this example: 
StringLiteral = '{String Ch 2}*' 
z
Enclosed in single-quotes, containing paired single-quotes that are each interpreted as a single 
single-quote character as illustrated by this example: 
StringLiteral = '(''|{String Ch 2})*' 
Each string constant in an expression or parameter list can be constructed using any of these rules, 
independently of other string constants. 
Integer constants contain no decimal point: 
IntegerLiteral = {Digit}+ 
Real constants contain a decimal point: 
RealLiteral = {Digit}+.{Digit}+ 
Identifiers (variable, constant, and event parameter names) must begin with a letter or underscore, 
and continue with zero or more alphanumeric characters and/or underscores: 
Id = {ID Head}{ID Tail}* 
Rules
Variable, constant, and event parameter references 
<IdValue> consists of one of these: 
V(Id) 
GC(Id) 
SV(Id) 
E(Id) 
<FilterIdValue> consists of one of these: 
FV (Id) 
FGC (Id) 
FSV (Id) 
FE (Id)

Expressions 
A scalar expression is either of a known type (Number, Date, or String), or its type is unknown. 
<Scalar Exp> consists of one of these: 
<Numeric-castable Exp> 
<Date Exp> 
<String Exp> 
<Typeless Exp> 
A numeric-castable expression is either Number, String, or an unknown type.
<Numeric-castable Exp> consists of one of these: 
<Numeric Exp> 
Boolean rules 
A Boolean expression is an OR-conjunction of one or more AND-conjunctions. 
<Boolean Exp> consists of one of these: 
<And Exp> 
<And Exp> OR <Boolean Exp> 
An AND expression is an AND-conjunction of one or more negatable predicates. 
<AND Exp> consists of one of these: 
<Not Exp> 
<Not Exp> AND <And Exp> 
A NOT expression is a negatable predicate. 
<Not Exp> consists of one of these: 
NOT <Predicate> 
<Predicate> 
A predicate consists of one of these: 
z
A comparison of like-typed expressions 
z
A call to a Boolean function 
z
A Boolean sub-expression enclosed in parentheses 
<Predicate> consists of one of these: 
<String Exp> LIKE <String Exp>

<String Exp> IN <Scalar Tuple> 
<String Exp> : <Scalar Tuple> 
<String Exp> !: <Scalar Tuple> 
<String Exp> = <String Exp> 
<String Exp> <> <String Exp> 
<String Exp> != <String Exp> 
<String Exp> > <String Exp> 
<String Exp> >= <String Exp> 
<String Exp> < <String Exp> 
<String Exp> <= <String Exp> 
<String Exp> LIKE <Typeless Exp> 
<String Exp> = <Typeless Exp> 
<String Exp> <> <Typeless Exp> 
<String Exp> != <Typeless Exp> 
<String Exp> > <Typeless Exp> 
<String Exp> >= <Typeless Exp> 
<String Exp> < <Typeless Exp> 
<String Exp> <= <Typeless Exp> 
<Typeless Exp> LIKE <String Exp> 
<Typeless Exp> = <String Exp> 
<Typeless Exp> <> <String Exp> 
<Typeless Exp> != <String Exp> 
<Typeless Exp> > <String Exp> 
<Typeless Exp> >= <String Exp> 
<Typeless Exp> < <String Exp> 
<Typeless Exp> <= <String Exp> 
<Date Exp> IN <Scalar Tuple> 
<Date Exp> : <Scalar Tuple> 
<Date Exp> !: <Scalar Tuple> 
<Date Exp> = <Date Exp> 
<Date Exp> <> <Date Exp> 
<Date Exp> != <Date Exp> 
<Date Exp> > <Date Exp> 
<Date Exp> >= <Date Exp> 
<Date Exp> < <Date Exp> 
<Date Exp> <= <Date Exp> 
<Date Exp> = <Typeless Exp> 
<Date Exp> <> <Typeless Exp> 
<Date Exp> != <Typeless Exp> 
<Date Exp> > <Typeless Exp> 
<Date Exp> >= <Typeless Exp> 
<Date Exp> < <Typeless Exp> 
<Date Exp> <= <Typeless Exp> 
<Typeless Exp> = <Date Exp> 
<Typeless Exp> <> <Date Exp> 
<Typeless Exp> != <Date Exp> 
<Typeless Exp> > <Date Exp> 
<Typeless Exp> >= <Date Exp>

<Typeless Exp> < <Date Exp> 
<Typeless Exp> <= <Date Exp> 
<Numeric Exp> IN <Scalar Tuple> 
<Numeric Exp> : <Scalar Tuple> 
<Numeric Exp> !: <Scalar Tuple> 
<Numeric Exp> = <Numeric Exp> 
<Numeric Exp> <> <Numeric Exp> 
<Numeric Exp> != <Numeric Exp> 
<Numeric Exp> > <Numeric Exp> 
<Numeric Exp> >= <Numeric Exp> 
<Numeric Exp> < <Numeric Exp> 
<Numeric Exp> <= <Numeric Exp> 
<Numeric Exp> = <Typeless Exp> 
<Numeric Exp> <> <Typeless Exp> 
<Numeric Exp> != <Typeless Exp> 
<Numeric Exp> > <Typeless Exp> 
<Numeric Exp> >= <Typeless Exp> 
<Numeric Exp> < <Typeless Exp> 
<Numeric Exp> <= <Typeless Exp> 
<Typeless Exp> = <Numeric Exp> 
<Typeless Exp> <> <Numeric Exp> 
<Typeless Exp> != <Numeric Exp> 
<Typeless Exp> > <Numeric Exp> 
<Typeless Exp> >= <Numeric Exp> 
<Typeless Exp> < <Numeric Exp> 
<Typeless Exp> <= <Numeric Exp> 
<Typeless Exp> IN <Scalar Tuple> 
<Typeless Exp> : <Scalar Tuple> 
<Typeless Exp> !: <Scalar Tuple> 
<Typeless Exp> = <Typeless Exp> 
<Typeless Exp> <> <Typeless Exp> 
<Typeless Exp> != <Typeless Exp> 
<Typeless Exp> > <Typeless Exp> 
<Typeless Exp> >= <Typeless Exp> 
<Typeless Exp> < <Typeless Exp> 
<Typeless Exp> <= <Typeless Exp> 
TRUE 
FALSE 
ANYHANDLERSFAILED ( ) 
HANDLERSYNCHRONOUS ( )
HANDLERSUSPENDS ( )
HANDLERTRANSACTIONAL ( )
HANDLERIGNORESFAILURE ( )
VOTINGDISPARITY (<EventActionRef>) 
VOTINGTIE (<EventActionRef>) 
HASBEGUN (<EventActionRef>) 
HASFINISHED (<EventActionRef>) 
INSIDEDATABASE ( )

PROPERTYMODIFIED (<String Exp>)
PROPERTYMODIFIED (<Typeless Exp>)
Sub-expression: 
(<Boolean Exp>) 
Typeless rules 
A typeless expression is a concatenation or sum of elements whose type (between String, Numeric, 
and Date) we cannot distinguish without context. 
<Typeless Exp> consists of one of these: 
<Typeless Exp> + <Typeless Value> 
<Typeless Value> 
A typeless value can be any of these: 
z
A variable reference 
z
A function call whose type cannot be determined without context 
z
A typeless sub-expression enclosed in parentheses 
<Typeless Value> consists of one of these: 
<IdValue> 
IF (<Boolean Exp>, <Typeless Exp>, <Typeless Exp>) 
DBFUNCTION (<Parameter List>)

Framework event parameters: 
PROPERTY (Id, <Numeric Exp>, <String Exp>) 
PROPERTY (Id, <Numeric Exp>, <Typeless Exp>) 
PROPERTY (Id, <Typeless Exp>, <String Exp>) 
PROPERTY (Id, <Typeless Exp>, <Typeless Exp>) 
P (Id, <Numeric Exp>, <String Exp>) 
P (Id, <Numeric Exp>, <Typeless Exp>) 
P (Id, <Typeless Exp>, <String Exp>) 
P (Id, <Typeless Exp>, <Typeless Exp>) 
PROPERTY (<Numeric Exp>, <String Exp>) 
PROPERTY (<Numeric Exp>, <Typeless Exp>) 
PROPERTY (<Typeless Exp>, <String Exp>) 
PROPERTY (<Typeless Exp>, <Typeless Exp>) 
P (<Numeric Exp>, <String Exp>) 
P (<Numeric Exp>, <Typeless Exp>) 
P (<Typeless Exp>, <String Exp>) 
P (<Typeless Exp>, <Typeless Exp>) 
PROPERTY (<String Exp>) 
PROPERTY (<Typeless Exp>) 
P (<String Exp>) 
P (<Typeless Exp>) 
METHODPARM (<Numeric Exp>)
METHODPARM (<Typeless Exp>)
Sub-expression: 
(<Typeless Exp>) 
Parameter list 
A parameter list is a comma-separated list of scalar expressions of any type. 
<Parameter List> consists of one of these: 
<Scalar Exp> 
<Scalar Exp>, <Parameter List> 
Scalar tuples 
A scalar tuple is a parenthesized set of one or more scalar expressions. 
<Scalar Tuple> consists of this: 
(<Scalar Expr Set>)

Scalar expression sets 
A scalar expression set is a semi-colon-separated list of one or more scalar expressions, as in this. 
<Scalar Expr Set> consists of one of these: 
<Scalar Exp>; <Scalar Expr Set> 
<Scalar Exp> 
String rules
A string expression is a concatenation of expressions of type String or of unknown type (see the 
second restriction under Restrictions on page 132). 
<String Exp> consists of one of these: 
<String Value> 
<String Exp> + <String Value> 
<String Exp> + <Typeless Value> 
A string value can be any of these: 
z
A string literal 
z
A quoted variable reference 
z
A function call returning a string value 
z
A string sub-expression enclosed in parentheses 
<String Value> consists of one of these: 
StringLiteral 
<FilterIdValue> 
IF (<Boolean Exp>, <String Exp>, <String Exp>) 
IF (<Boolean Exp>, <String Exp>, <Typeless Exp>) 
IF (<Boolean Exp>, <Typeless Exp>, <String Exp>) 
String built-in functions: 
CLIENTSUBSTITUTE (<String Exp>, <String Expr List>)
CLIENTSUBSTITUTE (<Typeless Exp>, <String Expr List>)
SUBSTITUTE (<String Exp>, <String Expr List>) 
SUBSTITUTE (<Typeless Exp>, <String Expr List>) 
SUBSTRING (<String Exp>, <Numeric Exp>) 
SUBSTRING (<String Exp>, <Typeless Exp>) 
SUBSTRING (<String Exp>, <Numeric Exp>, <Numeric Exp>) 
SUBSTRING (<String Exp>, <Numeric Exp>, <Typeless Exp>) 
SUBSTRING (<String Exp>, <Typeless Exp>, <Numeric Exp>) 
SUBSTRING (<String Exp>, <Typeless Exp>, <Typeless Exp>) 
SUBSTRING (<Typeless Exp>, <Numeric Exp>)

SUBSTRING (<Typeless Exp>, <Typeless Exp>) 
SUBSTRING (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
SUBSTRING (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
SUBSTRING (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
SUBSTRING (<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
UPPER (<String Exp>) 
UPPER (<Typeless Exp>) 
LOWER (<String Exp>) 
LOWER (<Typeless Exp>) 
REPLACE (<String Exp>, <String Exp>, <String Exp>) 
REPLACE (<String Exp>, <String Exp>, <Typeless Exp>) 
REPLACE (<String Exp>, <Typeless Exp>, <String Exp>) 
REPLACE (<String Exp>, <Typeless Exp>, <Typeless Exp>) 
REPLACE (<Typeless Exp>, <String Exp>, <String Exp>) 
REPLACE (<Typeless Exp>, <String Exp>, <Typeless Exp>) 
REPLACE (<Typeless Exp>, <Typeless Exp>, <String Exp>) 
REPLACE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
Event attributes: 
EVENTNAME() 
ORIGINATOR() 
CONFIGNAME() 
EVENTSTATE() 
EVENTTITLE() 
ACTIONTYPENAME ()
VOTINGRESULT (<EventActionRef>) 
RECIPIENTLIST (<EventActionRef>) 
RESPONDERLIST (<EventActionRef>) 
RESPONDERLIST (<EventActionRef>, <String Exp>) 
RESPONDERLIST (<EventActionRef>, <Typeless Exp>) 
Environment attributes: 
APPNAME() 
COMPANYNAME() 
USERNAME() 
USERDESC() 
WORKINGDIR() 
FILECONTENTS (<String Exp>) 
FILECONTENTS (<Typeless Exp>) 
NEWGUID()

Framework event parameters: 
IDO() 
INITIATOR() 
FILTERSTRING() 
LOADFLAGS() 
PROPERTYNAMES() 
POSTQUERYACTIONS() 
CUSTOMINSERT() 
CUSTOMUPDATE() 
CUSTOMDELETE() 
VARIABLENAME() 
VARIABLEVALUE() 
FILTERPROPERTY (Id, <Numeric Exp>, <String Exp>) 
FILTERPROPERTY (Id, <Numeric Exp>, <Typeless Exp>) 
FILTERPROPERTY (Id, <Typeless Exp>, <String Exp>) 
FILTERPROPERTY (Id, <Typeless Exp>, <Typeless Exp>) 
FP (Id, <Numeric Exp>, <String Exp>) 
FP (Id, <Numeric Exp>, <Typeless Exp>) 
FP (Id, <Typeless Exp>, <String Exp>) 
FP (Id, <Typeless Exp>, <Typeless Exp>) 
FILTERPROPERTY (<Numeric Exp>, <String Exp>) 
FILTERPROPERTY (<Numeric Exp>, <Typeless Exp>) 
FILTERPROPERTY (<Typeless Exp>, <String Exp>) 
FILTERPROPERTY (<Typeless Exp>, <Typeless Exp>) 
FP (<Numeric Exp>, <String Exp>) 
FP (<Numeric Exp>, <Typeless Exp>) 
FP (<Typeless Exp>, <String Exp>) 
FP (<Typeless Exp>, <Typeless Exp>) 
FILTERPROPERTY (<String Exp>) 
FILTERPROPERTY (<Typeless Exp>) 
FP (<String Exp>) 
FP (<Typeless Exp>) 
METHOD ( )
FILTERMETHODPARM (<Numeric Exp>)
FILTERMETHODPARM (<Typeless Exp>)
FILTER (<String Exp>) 
FILTER (<Typeless Exp>) 
CAST (<Scalar Exp> AS STRING) 
Sub-expression:

(<String Exp>) 
<Message Conversation> 
String expression lists 
A string expression list is an ordered, comma-separated list of string and/or scalar expressions. 
<String Expr List> consists of one of these: 
<Scalar Exp> 
<String Expr List>, <Scalar Exp> 
Message conversations 
A message conversation is one or more MESSAGE() calls separated by 
| newline/concatenation operators. 
<Message Conversation> consists of one of these: 
<Message> 
<Message Conversation> | <Message> 
Messages 
A message is the MESSAGE function surrounding a parenthesized, ordered, comma-separated list of 
string and/or typeless expressions. 
<Message> consists of one of these: 
MESSAGE (<String Exp>) 
MESSAGE (<Typeless Exp>) 
MESSAGE (<String Exp>, <String Expr List>) 
MESSAGE (<Typeless Exp>, <String Expr List>) 
Numeric rules
<Numeric Exp> consists of this: 
<Sum> 
Sums 
A sum is a chain of sums and/or differences: 
<Sum> consists of one of these:

<Addend> 
<Sum> + <Addend> 
<Sum> – <Addend> 
Addends 
An addend is a negatable expression, or a product. 
These can be added to or subtracted from one another without parentheses surrounding each, due to 
the accepted arithmetic operator precedence. 
<Addend> consists of one of these: 
<Negate Exp>
<Addend> * <Negate Exp> 
<Addend> / <Negate Exp> 
Negatable expressions 
A negatable expression is a numeric value with or without a unary negative. 
<Negate Exp> consists of one of these: 
– <Numeric Value> 
<Numeric Value> 
- <IdValue> 
Numeric values 
A numeric value can be any of these: 
z
A numeric constant 
z
A function call returning a numeric value 
z
A numeric sub-expression enclosed in parentheses 
<Numeric Value> consists of one of these: 
IntegerLiteral 
RealLiteral 
IF (<Boolean Exp>, <Numeric Exp>, <Numeric Exp>) 
IF (<Boolean Exp>, <Numeric Exp>, <Typeless Exp>) 
IF (<Boolean Exp>, <Typeless Exp>, <Numeric Exp>) 
Numeric built-in functions: 
DATEDIFF (<TimeInterval>, <Date Exp>, <Date Exp>) 
DATEDIFF (<TimeInterval>, <Date Exp>, <Typeless Exp>)

DATEDIFF (<TimeInterval>, <Typeless Exp>, <Date Exp>) 
DATEDIFF (<TimeInterval>, <Typeless Exp>, <Typeless Exp>) 
DATEPART (<TimeInterval>, <Date Exp>) 
DATEPART (<TimeInterval>, <Typeless Exp>) 
LEN (<String Exp>) 
LEN (<Typeless Exp>) 
INSTR (<String Exp>, <String Exp>) 
INSTR (<String Exp>, <Typeless Exp>) 
INSTR (<Typeless Exp>, <String Exp>) 
INSTR (<Typeless Exp>, <Typeless Exp>) 
CEILING (<Numeric Exp>) 
CEILING (<Typeless Exp>) 
FLOOR (<Numeric Exp>) 
FLOOR (<Typeless Exp>) 
POWER (<Numeric Exp>, <Numeric Exp>) 
POWER (<Numeric Exp>, <Typeless Exp>) 
POWER (<Typeless Exp>, <Numeric Exp>) 
POWER (<Typeless Exp>, <Typeless Exp>) 
ROUND (<Numeric Exp>, <Numeric Exp>) 
ROUND (<Numeric Exp>, <Typeless Exp>) 
ROUND (<Typeless Exp>, <Numeric Exp>) 
ROUND (<Typeless Exp>, <Typeless Exp>) 
TRUNC (<Numeric Exp>, <Numeric Exp>) 
TRUNC (<Numeric Exp>, <Typeless Exp>) 
TRUNC (<Typeless Exp>, <Numeric Exp>) 
TRUNC (<Typeless Exp>, <Typeless Exp>) 
Event state attributes: 
EVENTREVISION ( )
HANDLERSEQ ( )
ACTIONSEQ ( )
Event attributes: 
RECIPIENTS (<EventActionRef>) 
RESPONDERS (<EventActionRef>) 
RESPONDERS (<EventActionRef>, <String Exp>) 
RESPONDERS (<EventActionRef>, <Typeless Exp>)

Framework event parameters: 
RECORDCAP() 
ROWS (Id) ROWS ( )
METHODPARMS ( )
CAST (<Scalar Exp> AS NUMBER) 
Sub-expression: 
(<Numeric Exp>) 
Date rules 
A date expression is a date value (because there are no natural arithmetic date operators). 
<Date Exp> consists of this: 
<Date Value> 
A date value is a function call returning a date value, or a date sub-expression enclosed in 
parentheses. 
<Date Value> consists of one of these: 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>)

DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>)

DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>)

DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Numeric Exp>, <Typeless Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>)

DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Numeric Exp>, <Typeless Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>)

DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Numeric Exp>, <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Numeric Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Numeric Exp>, <Numeric Exp>, <Typeless Exp>)

DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Numeric Exp>, <Typeless Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Typeless Exp>, <Numeric Exp>, <Typeless Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Numeric Exp>) 
DATE (<Typeless Exp>, <Typeless Exp>, <Typeless Exp> ',' <Typeless Exp>, 
<Typeless Exp>, <Typeless Exp>, <Typeless Exp>) 
CURDATETIME() 
DATEADD (<TimeInterval>, <Numeric Exp>, <Date Exp>) 
DATEADD (<TimeInterval>, <Numeric Exp>, <Typeless Exp>) 
DATEADD (<TimeInterval>, <Typeless Exp>, <Date Exp>) 
DATEADD (<TimeInterval>, <Typeless Exp>, <Typeless Exp>) 
BEGINDATE() 
CAST (<Scalar Exp> AS DATE) 
Sub-expression: 
(<Date Exp>) 
Date enumerations 
<TimeInterval> consists of one of these: 
<DatePartYear> 
<DatePartQuarter> 
<DatePartMonth> 
<DatePartDayOfYear> 
<DatePartDay> 
<DatePartWeek> 
<DatePartWeekDay> 
<DatePartHour> 
<DatePartMinute> 
<DatePartSecond> 
<DatePartMillisecond> 
<DatePartYear> consists of one of these: 
year 
yy

yyyy 
<DatePartQuarter> consists of one of these: 
quarter 
qq 
q 
<DatePartMonth> consists of one of these: 
month 
mm 
m 
<DatePartDayOfYear> consists of one of these: 
dayofyear 
dy 
y 
<DatePartDay> consists of one of these: 
day 
dd 
d 
<DatePartWeek> consists of one of these: 
week 
wk 
ww 
<DatePartWeekDay> consists of one of these: 
weekday 
dw 
<DatePartHour> consists of one of these: 
hour 
hh

<DatePartMinute> consists of one of these: 
minute 
mi 
n 
<DatePartSecond> consists of one of these: 
second 
ss 
s 
<DatePartMillisecond> consists of one of these: 
millisecond 
ms 
Restricted arguments 
<EventActionRef> consists of this: 
IntegerLiteral 
Keyword paren lists 
A keyword paren list is one or more "KEYWORD(value)" statements separated by whitespace. 
<KeywordParenList> consists of one of these: 
<KEYWORD(value)> 
<KEYWORD(value)> ... <KEYWORD(value)> 
For a complete list and description of KEYWORD(value) statements as they relate to action types, 
see Event action parameters on page 126
Enumerations 
These lists of keywords can be used with ACTION( ), VOTINGRULE( ), and TASKSTATUS( ) 
expressions.

ACTION( ) 
<SaveAction> consists of one of these: 
<SaveActionInsert> 
<SaveActionUpdate> 
<SaveActionDelete> 
<SaveActionInsert> consists of this: 
INSERT 
<SaveActionUpdate> consists of this: 
UPDATE 
<SaveActionDelete> consists of this: 
DELETE 
VOTINGRULE( ) 
<VotingRule> consists of one of these: 
<VotingRuleMajority> 
<VotingRulePlurality> 
<VotingRuleConditionalPlurality> 
<VotingRuleMinimumCount> 
<VotingRuleMinimumPercentage> 
<VotingRuleEarliestResponse> 
<VotingRulePreferredChoice> 
<VotingRuleMinimumCountPreferredChoice>
<VotingRuleMinimumPercentagePreferredChoice>
<VotingRuleMajority> consists of this: 
Majority 
<VotingRulePlurality> consists of this: 
Plurality 
<VotingRuleConditionalPlurality> consists of this: 
ConditionalPlurality 
<VotingRuleMinimumCount> consists of this: 
MinimumCount 
<VotingRuleMinimumPercentage> consists of this: 
MinimumPercentage

<VotingRuleEarliestResponse> consists of this: 
EarliestResponse 
<VotingRulePreferredChoice> consists of this: 
PreferredChoice 
<VotingRuleMinimumCountPreferredChoice> consists of this: 
MinimumCountPreferredChoice
<VotingRuleMinimumPercentagePreferredChoice> consists of this: 
MinimumPercentagePreferredChoice
TASKSTATUS( ) 
<InitialTaskStatus> consists of one of these: 
<TaskStatusReady> 
<TaskStatusWaiting> 
<TaskStatusReady> consists of this: 
READY 
<TaskStatusWaiting> consists of this: 
WAITING

### Appendix D: Sample Stored Procedures
*Pages 157-158*

D
Appendix D: Sample Stored Procedures
The sample stored procedures in this appendix provide sample code and function usage. 
Passing parameters to a synchronous event 
SET @MyEventParmId = NEWID() 
EXEC InsertEventInputParameterSp @MyEventParmId, 'Parameter1', @Variable1 
EXEC InsertEventInputParameterSp @MyEventParmId, 'Parameter2', @Variable2 
EXEC InsertEventInputParameterSp @MyEventParmId, 'OutParameter3', NULL, 1 
EXEC FireEventSp 'EventName', @MyEventParmId 
PRINT dbo.EventOutputParameterValue(@MyEventParmId, 'OutParameter3') 
Calling a synchronous event within a transaction and 
handling failure 
First, determine the current site, after which you must name a configuration, by convention: 
DECLARE @Site SiteType 
SELECT @Site = site FROM parms 
Then determine the current SessionId: 
DECLARE @SessionId RowPointerType 
SET @SessionId = dbo.SessionIdSp() 
Finally, add the procedure code: 
BEGIN TRANSACTION 
UPDATE coitem 
SET due_date = dbo.CalcDueDate(@Parm1, @Parm2) 
WHERE coitem.co_num = @CoNum

AND coitem.co_line = @CoLine 
AND coitem.co_release = @CoRelease 
SET @MyEventParmId = NEWID() 
EXEC InsertEventInputParameterSp @MyEventParmId, 'CoNum', @CoNum 
EXEC InsertEventInputParameterSp @MyEventParmId, 'CoLine', @CoLine 
EXEC InsertEventInputParameterSp @MyEventParmId, 'CoRelease', @CoRelease 
DECLARE 
@anyHandlersFailed [tinyint], 
@result [nvarchar](4000), 
@Infobar [nvarchar](4000) 
EXEC @Severity = FireEventSp 
@eventName = SetCoitemDueDate', 
@configName = 'SyteLine', 
@sessionID = @SessionID, 
@eventTrxId = null, 
@eventParmId = @MyEventParmID OUTPUT, 
@transactional = 0, 
@anyHandlersFailed = @anyHandlersFailed output, 
@result = @result output, 
@Infobar = @infobar output 
IF @Severity > 0 
BEGIN 
EXEC RaiseError @Infobar, @Severity 
ROLLBACK TRANSACTION 
END 
... 
COMMIT TRANSACTION

### Appendix E: Synchronization of Metadata
*Pages 159-186*

E
Appendix E: Synchronization of Metadata
This appendix discusses the various concepts and strategies for synchronizing metadata belonging to 
different owners, and provides a number of detailed examples. 
Overview and rationale 
Application event system metadata can come from three primary sources: 
z
The Infor system framework (Mongoose) 
z
Applications produced by Infor and/or Infor’s business partners or other authorized vendor 
developers 
z
End-customer development 
The ownership for the metadata from each of these sources is controlled by the Access As identifier. 
For more information on this identifier, see “About the Access As identifier” on page 31. 
Any of these sources can upgrade and reissue their metadata at times independent of the others. The 
upgrade process must: 
z
Update any changed handlers that they own. 
z
Insert any new handlers they might have created since the last version. 
z
Maintain other owners’ handlers and the relationships between them. 
Therefore, a synchronization mechanism is needed, to make sure that changes by one metadata 
owner do not adversely affect the functioning of another owner’s metadata. 
This mechanism is provided in two components: 
z
The Access As identifier (see “About the Access As identifier” on page 31) 
z
The App Metadata Sync and App Metadata Transport utilities, which both provide the capability to 
synchronize event metadata belonging to different owners. 
Using these utilities, you can export your events and event handlers and make them available for 
import by other metadata owners. You can also use these utilities to import your own or others’ 
metadata into your system. 
For more information about these utilities, see the online help for each utility.

The inherent hierarchy of metadata 

however, an inherent hierarchy, based on the normal production flow and use of the system software. 
As illustrated in this diagram, Infor’s framework developers are the first to develop event system 
objects. Other Infor application developers then can add their own event system objects, as can 
authorized business partners and other vendor developers. Finally, end customers can make custom 
modifications and develop their own custom event system objects.  
In reality, the system is designed so that no metadata owner can modify or delete the metadata of 
another owner. So, in that sense, they are all equal. However, this real-time production flow creates 
an inherent hierarchy that allows us to think of them as "higher-level" (that is, Infor) and "lower-level" 
(that is, end-customer) owners. 
With that in mind, we can state these general rules: 
z
Lower-level owners can insert their handlers between two higher-level handlers for the same 
event. 
z
In many cases, lower-level owners can override higher-level handlers. 
There is, however, an option for higher-level owners to disallow overrides for individual handlers. 
z
Higher-level handlers that are overridden remain in the metadata store but are marked as 
Inactive. 
This means, among other things that, if the lower-level handler is later deleted, the higher-level 
handler is still available and can become active again. 
Chronology rules allow downstream owners to integrate and control the sequence of their events and 
handlers with respect to those upstream. For more information, see “Detailed examples” on 
page 161.

Maintaining handler IDs through metadata updates 
Each event handler is identified with a unique (and hidden) ID, which is referenced by the Keep With 
field on the Event Handlers form. This ID, rather than the actual Handler Sequence number, 
becomes the "fixed" reference point for that handler. This means that an event handler owner does 
not need to worry about maintaining the Handler Sequence numbers across releases: The system 
takes care of it automatically, by preserving the hidden ID number and reassigning Handler 
Sequence numbers as required. 
After each insertion, update, or deletion of a handler, and during a merge performed by the App 
Metadata Sync utility or the App Metadata Transport utility, the system calculates new integers, if 
necessary, for display in the Handler Sequence field. The underlying ID, however, remains 
unchanged. When a handler is deactivated and another added in the same position, the new handler 
gets a new ID. 
Protecting running events from metadata changes 
Once an event handler begins executing, it is essential to prevent changes to its attributes and 
actions. Otherwise, unpredictable behavior could result, especially if actions are resequenced. 
One way to prevent these changes would be to make a copy of all active, non-obsolete handlers and 
their actions each time an event is triggered and control execution from this copy. However, that 
method would result in the persistence of a great number of identical copies, assuming that handlers 
are modified much less frequently than they are executed. 
Since the system stores state data separately from metadata, it is sufficient to make a copy only when 
the metadata changes, and furthermore only when the corresponding event is triggered and a copy of 
the last metadata modifications has not yet been made. 
In other words, handler metadata for an event can be created and edited as many times as 
necessary. The first time the event is triggered, a copy of the last saved metadata is made. This copy 
is called an event revision. The execution of the event's handlers is then controlled by the event 
revision and not by the original metadata (which happen to be identical at this point). 
The event can be triggered as many times as necessary, all the time controlled by this event revision, 
as long as no intervening modifications have been made to the original metadata. 
After one or more metadata edits have been saved, though, the next time the event is triggered, the 
system copies a new event revision from the last-saved metadata. 
For more information about event revisions, see “Events and event handler revisions” on page 28. 
Detailed examples 
This section provides three detailed examples of how sequencing and synchronization work in the 

Using specific chronology 
The primary way for a lower-level handler creator to resequence existing handlers (from higher-level 
owners) is to use what is known as specific chronology. That is, the handler’s creator can attach the 
new handler to an existing handler and specify the order in which the two handlers are to execute with 
respect to each other. 
The mechanism used to do this are the Keep With and Chronology fields on the Event Handlers 
form. These fields allow you to specify whether your handler should run before, after, or in place of the 
handler it is associated with, as in this example. 
For more information about the Keep With and Chronology fields, see the online help for those 
fields. 
Infor creates a framework event with three handlers 
The Infor framework team creates an event, FrameEvent, and creates three event handlers that 
execute in order when the event is generated. 
This event and these handlers are all included with the application software when it ships. 
Note that, if a "lower-level" developer wants to add or modify handlers, these rules apply: 
z
Lower-level handler creators cannot change the sequence of higher-level handlers. 
z
Any handlers lower-level creators want to use that will affect the sequence in specific ways 
must be associated with a particular, already-existing handler, using the Keep With and 
Chronology fields.

A business partner creates an additional handler 
An Infor business partner decides to add a handler that will execute just after the first framework 
handler. The business partner creates the event handler and uses the Keep With and 
Chronology fields to keep their handler with ID 1 (S1) and to execute After that handler. 
The sequence is now this:  
Note that, when the new event handler is saved, the system automatically assigns new Handler 
Sequence numbers, so that you can tell which handler executes in what order. 
The business partner uses the App Metadata Sync or App Metadata Transport utility to export the 
new metadata, along with the existing metadata, to a file that can be imported by the end-
customer. 
The business partner then sells the add-on product to the end-customer. The add-on product 
includes this file, along with any product code the business partner has developed. 
The end-customer creates three more handlers 
When the end-customer receives the add-on software from the third-party business partner, in 
addition to whatever other software installation procedures the customer must perform, the 
customer must also use the App Metadata Sync or App Metadata Transport utility to import the 
event metadata from the business partner. 
The end-customer now decides to use a different handler in place of the second framework 
handler. The customer also wants two custom handlers to run just before the third framework 
handler. To accomplish this, the customer:

z
Creates a handler and uses the Keep With field to assign this handler to ID 2 (S2). In the 
Chronology field, the customer selects Instead. 
z
Creates a second handler and uses the Keep With field to assign this handler to ID 3 (S3). In 
the Chronology field, the customer selects Before. 
z
Creates a third handler and uses the Keep With field to also assign this handler to ID 3 (S3). 
In the Chronology field, again the customer selects Before. 
After saving their new handlers with the existing handlers, the sequence is now this:  
Again, note that, when the customer saves the new handlers, the system automatically assigns 
and displays the correct Handler Sequence number on the Event Handlers form. The 
underlying Handler IDs, however, remain unchanged. 
Note that event handler S2 is now inactive and does not execute at all. It is still in the system, but 
the system ignores it in favor of the new customer handler. 
Note also that the custom handlers C2 and C3 execute in that order unless you use the Up / 
Down buttons on the Event Handler Sequence form to alter the default order.

Using non-specific chronology 
A second way for downstream developers to affect the sequence of handlers is with the use of non-
specific chronology. Non-specific chronology allows developers to indicate that a particular handler 
should always execute either first or last. 
This is done by selecting either the First or Last option from the Chronology drop-down field, as in 
this example. 
Infor creates an event with no handler 
The Infor development team adds code to generate a new application event (AppEvent) before a 
certain transaction posting is performed. 
The transaction data is passed into the event and received from the event, so that any 
downstream subscribers can test and modify the values before the posting is performed if they 
want. An event failure is trapped and aborts the posting, displaying the error message returned by 
the event. Infor adds no event handlers for the event at this time.  
The product is then released. The event is now published and available to downstream 
developers who install this product. 
An end-customer creates a handler 
An end-customer installs the software and decides to create a handler (EC1) to validate that the 
posting data is within a certain range. If it detects an out-of-range condition, the handler fails the 
event and aborts the posting.

At this point, the sequence is this:  
Because no upstream handlers exist yet (and the end-customer is the furthest downstream 
developer), a specific chronology cannot be specified at this time. 
A business partner creates an add-on product 
In the meantime, an Infor business partner creates an add-on product that stores custom 
parameters that can be used to adjust the transaction data before posting. They add their own 
handler (BP1) to input, adjust, and output the data. 
In the Chronology field, they select First to indicate that handler BP1 should run before: 
z
Any existing, downstream handlers with no specified chronology that might already exist for 
this published event 
z
Any future upstream or peer handlers 
Note: A specific chronology (Before, After, Instead) takes precedence over a non-
specific one (First and Last).

With this add-on product, at the business partner level, the sequence is now this:  
The end-customer installs the business partner’s add-on product 
Now the end-customer purchases and installs the add-on from the Infor business partner and 
uses the App Metadata Sync or App Metadata Transport utility to synchronize the metadata from 
the business partner with their own.

Because the business partner specified that their handler should always run first, the sequence is 
now this:  
The end-customer rearranges the sequence 
After installing the business partner’s add-on product, the end-customer decides that their handler 
really should run before the business partner’s. So the end-customer uses the Keep With and 
Chronology fields to associate handler EC1 with the business partner’s handler (BP1) and to 
execute Before it.

After saving the event handler EC1, the sequence is this: 
This is possible because a specific chronology designation (see “Using specific chronology” on 
page 162) takes precedence over a non-specific chronology. 
The end-customer decides to add another handler 
After this, the end-customer adds a new handler (EC2) to save the final, adjusted transaction data 
into a data warehouse. They use the Keep With and Chronology fields to associate the new 
handler with the business parther’s handler, specifying that the new one execute After the 
business partner’s (BP1).

After saving the new event handler, the sequence is this:  
Another business partner adds a handler 
Independently of all this, a second Infor business partner installs the standard Infor software and 
decides to add another event handler for their add-on product. This event handler (AV1) is to post 
additional information to the journal based on the transaction data that was specified. 
Because this handler should run after all transaction data has been processed, the business 
partner specifies in the Chronology field that event handler AV1 should execute Last.

At this point, the flow looks similar to the first business partner’s add-on flow:  
However, the effect of designating this handler to run Last is quite different.

The end-customer adds the second business partner’s handler 
Finally, the end-customer purchases and installs the second business partner’s add-on product. 
After using the App Metadata Sync or App Metadata Transport utility to synchronize the new 
metadata with the existing metadata, the flow now proceeds as follows:  
Note that, even without the Last designation, in this case, handler AV1 would have executed last 
simply because the handler BP1 is designated to execute First, and the other two handlers are 
both "attached" to BP1.

Performing upgrades 
It is likely that at some point in the future, Infor will make changes to the existing events and handlers, 
and these changes will be included in an upgrade. This poses a few problems and questions. The 
upgrade process must: 
z
Update any changed Infor handlers and insert new ones while maintaining custom handlers 
belonging to business partners and end-customers. 
z
Keep custom handlers in the correct sequence with Infor’s handlers (especially for overrides) 
beyond the point where Infor inserts a new handler. 
To illustrate how this works, we return to the previous examples (in “Using specific chronology” on 
page 162 and “Using non-specific chronology” on page 165). 
Continuing the specific chronology example… 
After the end-customer has installed the Infor software and the business partner add-on product 
and added its own custom handlers, Infor introduces a new version in which one of the original 
base handlers (S2) has been modified and a new one, S4, has been added between S2 and S3. 
The new base flow in the upgrade is illustrated in this diagram:

Note that, when this version is released, the numbers actually displayed in the Handler 
Sequence field of the Event Handlers form are as follows: 
Note that what was previously the third event handler in the flow (S3), now appears as 4 in the 
Handler Sequence field. This is because, when the Infor developer saves the new handler, the 
system automatically assigns the correct Handler Sequence number, without changing the 
underlying Handler ID number. 
Handler ID 
Handler Sequence number 
S1 

S2 

S3

S4 

The end-customer now installs the new Infor upgrade and uses the App Metadata Sync or App 
Metadata Transport utility to import and synchronize the updated metadata for this event. After the 
integration is complete, the new end-customer sequence is this:  
Note: 
z
Infor handler S2 has been updated. In this case, the update does not run, because of the end-
customer handler C1, which replaces it. But the changes are there (stored as handler 
metadata) and available if the end-customer should ever decide to delete handler C1. 
z
The synchronization process inserts the new Infor handler between end-customer handlers 
C1 and C2. This is because end-customer handler C1 is "attached" to Infor handler S2; end-

customer handlers C2 and C3 are "attached" to Infor handler S3; and the new Infor handler 
has been inserted between S2 and S3. 
Continuing the non-specific chronology example… 
(Starting at the end of “Using non-specific chronology” on page 165:) After the end-customer has 
installed the Infor software and both business partner add-on products, Infor introduces a new 
version in which a new handler to validate data formats has been added and designated to run 
First. The new base flow in the upgrade is illustrated in this diagram:  
Note that this new upgrade will now cause the event to be generated and check data formats 
whenever the appropriate transaction is posted. This is different, because before the Infor base 
version of this event did nothing. 
Now the end-customer installs the Infor upgrade and uses the App Metadata Sync or App 
Metadata Transport utility to import and synchronize the new handler metadata with the existing 
metadata for this event. Because the business partner handler BP1 is marked to execute First, 
that handler and all handlers "attached" to it (EC1 and EC2) are placed at the beginning. Because 
the business partner handler AV1 is marked to execute Last, that handler is placed at the end. 
Because the Infor handler SL1 is not marked to execute in any particular order, it is inserted 
between EC2 (which is attached to BP1) and AV1.

After the integration is complete, the new handler sequence is as follows:  
Overriding others’ handlers 
As demonstrated briefly in “Using specific chronology” on page 162, downstream event handler 
creators can create handlers that, in effect, replace an upstream handler. This is done primarily with

the use of the Instead option in the Chronology field on the Event Handlers form. This option allows 
multiple overriding handlers to coexist. In other words, this option is considered a non-exclusive 
override. 
There is also a second option for situations where a handler’s creator might want to override all other 
handlers, regardless of who owns them or when they were added to the sequence. This is done using 
the Exclusively (instead) option in the second Keep With field. This option is considered an 
exclusive override. 
Non-exclusive overrides 
In this example, the Infor application development team creates an application event and adds an 
event handler, SL1, for it.  
The application is released with this event metadata included as part of the standard product. 
An Infor business partner installs the software with this event metadata. They decide, however, that 
they want to replace the standard Infor event handler with one of their own. So they create handler 
BP1 and select Instead in the Chronology field on the Event Handlers form. After saving their 
handler, the sequence is as follows: 
Notice that this effectively bypasses and deactivates the original Infor event handler, SL1. 
The business partner then releases the add-on product with this new event handler in place.

In the meantime, a second Infor business partner does the same thing. For the sake of the example, 
the second business partner’s handler is labeled AV1. 
Now suppose that a customer purchases and installs the standard Infor product. At this point, the 
sequence is the same as what both business partners received originally: 
When the event is generated, the Infor event handler executes. 
The customer then purchases and installs the add-on product from the first business partner. At this 
point, the sequence is the same as the first business partner’s. The App Metadata Sync or App 
Metadata Transport utility recognizes the override of BP1 and automatically deactivates the Infor 
handler SL1. 
But then, the customer also purchases the second business partner’s add-on product and installs it. 
The App Metadata Sync or App Metadata Transport utility recognizes the new override of AV1 and

allows both overrides to coexist. When the event is generated, both handlers BP1 and AV1 execute. 
The sequence now looks something like this:  
Note that, in this case, there is no reliable way to know the precise order in which event handlers BP1 
and AV1 will execute, since they coexist at the same level in the sequence and execute 
independently of one another. 
Exclusive overrides 
To continue the example, suppose that the Infor application development team now adds another 
event handler, SL2, for the same event. When Infor releases the upgrade, the sequence for this event 
now looks like this: 
The first business partner installs the upgrade using the App Metadata Sync or App Metadata 
Transport utility. Once again, they decide they want to override the new Infor handler with one of their

own. So they create a new handler, BP2, and assign it to run Instead of SL2. When they release the 
new version of their add-on product, the sequence for this event now looks like this: 
Note that, so far, this is typical non-exclusive override behavior. 
The second business partner does the same thing as the first, with one exception: They specify that 
the new handler, AV2, is to execute Exclusively Instead, regardless of any other handlers that might 
exist at that point in the sequence. When they release their new version, the sequence for this event 
looks very similar to that of the first business partner: 
However, the outcome is quite different. 
Suppose the customer now installs the Infor software upgrade and tries to install the upgrades for 
both business partners as well. All goes well until the customer tries to install the new version of the 
second business partner’s add-on product. When the customer tries to synchronize the event

metadata from the second business partner, the App Metadata Sync or App Metadata Transport utility 
generates an error, because the handler AV2 is set to execute exclusively, which puts it in conflict with 
the first business partner’s handler BP2. The two cannot coexist. 
To resolve the conflict, the customer would have to uninstall one of the business partner handlers and 
contact them for guidance. 
In practice, this should be a very rare occurrence. 
Disabling the ability to override 
Owners of "higher-level" handlers can designate that their handlers cannot be overridden. 
Downstream developers cannot use a Chronology setting of Instead or Exclusive Instead with 
such a handler. 
To designate an event handler as not subject to being overridden, on the Event Handlers form, use 
the Overrideable check box. When this check box is cleared, no lower-level handlers can override 
that handler. In this case, the Instead and Exclusive Instead options are disabled for any other 
handlers (downstream) that use the Keep With field to associate those handlers with this handler. 
Dealing with obsolete handlers 
If you are an Infor or business partner developer, you must not delete handler metadata that has been 
exported and made available to other (downstream) metadata developers. This is because those 
developers might have their own metadata associated with your metadata, by means of the Keep 
With feature, before your next release. 
If your exported metadata removes a handler that is referenced by their handler's Keep With field, a 
broken link occurs during import. This forces the App Metadata Sync or App Metadata Transport utility 
to relegate the downstream developer’s handler to "free floating" status, meaning its sequence is less 
controllable. This is especially true if you—or an upstream developer whose handlers are referenced 
by your handlers' Keep With field—later resequence your handlers. 
Therefore, when a handler is no longer needed, on the Event Handlers form you should mark it as 
obsolete, by selecting the check box labeled Obsolete. This effectively and permanently deactivates 
the handler but leaves it in the sequence, so that associations with it do not get destroyed.

For example, consider this sequence of handlers:  
Suppose, after initially releasing this version of the metadata, Infor decides not to use the handler S1 
anymore. Because a business partner has associated handler A1 with this handler, if Infor simply 
deletes handler S1, a broken link occurs the next time the business partner or a customer who uses 
the business partner’s add-on product tries to install the upgraded metadata. Handler A1 is relegated

to a "free floating" status (as in this diagram), and unexpected consequences can result after 
subsequent resequencing or synchronizing operations.

So, rather than delete handler S1, Infor would mark it as Obsolete before the next release. Then, 
when the update is installed, the reference to handler S1 is not broken, though the system ignores it 
when handling this event, as in this diagram:

### Appendix F: Event Flow Options
*Pages 187-212*

F
Appendix F: Event Flow Options
The flow diagram in this appendix illustrates many of the possible ways an event can be generated 
and the types of flows that can result. This diagram highlights the differences between functionality 

Glossary 
Access As 
An identifier used to identify who created and owns a metadata object. This identifier is also used to 
control which metadata objects you can modify. You can modify only those metadata objects that are 
associated with the current Access As field value, as displayed on the Access As form.
For more information, see ”About the Access As identifier” on page 3-31. 
adjourning event 
An event action that must wait for an external stimulus before it can continue. When the system 
encounters an adjourning event action, the event handler state is set to retest or to time out after a 
specified time. The event system then processes it at the next opportunity and resumes. 
asynchronous event handler
An event handler designed to execute independently of other event handlers, and whose triggering 
process does not block while waiting for it to finish. These event handlers are sent to an event queue, 
from which they execute in FIFO order. 
See also "asynchronous event handler." 
database tier 
That part of the system framework that stores the actual data for: 
z
Rendering forms (the Forms database) 
z
Storing all customer business data (the Application database) 
Programs can also run in this tier, where they can access data very quickly without having to traverse 
network paths. 
For more information, see the "System Architecture" chapter in your System Administration Guide. 
end-customer 
The company that has bought and is using the Infor Mongoose software. They might also have 
bought one or more add-on products by Infor business partners to customize and enhance the 
performance of their system. 
Explorer 
A window in the application (similar to Windows Explorer) that displays folders containing form 
names, providing a means to find, organize, and open forms. Explorer is the default window when the 
application opens. To reopen Explorer if it is closed, select View > Explorer on the menu bar. 
event 
A uniquely named incident that can be triggered by: 
z
An action performed by somebody working in the system 
z
A particular condition that occurs while the system is running 
z
A certain value being exceeded in a database record

z
Another event or one its handlers 
z
Other, similar occurrences 
A particular event can possibly be triggered by multiple situations or conditions, and you can 
determine how the system responds to each situation. 
To be useful, an event must have one or more event handlers defined to respond to the event. 
For more information, see ”About events” on page 3-32. 
event action 
Metadata that specifies a unit of work to perform during the execution of an event handler. A single 
event handler can have multiple event actions. Depending on its action type, an event action can do 
such things as: 
z
Evaluate and compare expressions, using the results to select which event action of its event 
handler to perform next. 
z
Affect the event's visual state. 
z
Complete the event. 
z
Set event variables. 
z
Call methods. 
z
Perform other predefined tasks. 
For more information, see ”About event actions” on page 3-37. 
event action state 
A set of data that shows the current state of a running or finished event action. This data includes 
information about when the event action started running, its current status, the number of times it has 
run, and other information. 
event action type 
A designator that limits or directs what an event action can do. This designator essentially determines 
the unit of work that each event action performs. 
event global constant 
A named static value that event expressions can reference during processing of an event handler. 
event handler 
Metadata that defines a portion of work to be performed upon the firing of a particular event. Each 
event handler is uniquely identified in the system with the combination of an event name and a 
handler sequence number. Each event handler is comprised of one or more event actions and, 
optionally, an initial state. 
For more information, see ”About event handlers” on page 3-36. 
event handler state 
A set of data that shows the current state of a running or finished event handler. This data includes 
information about when the event handler started running, its current status, timeout settings, and 
other information.

event initial variable 
See "initial variable." 
event input parameter 
A named static value that is passed to an event upon its triggering. This value can be set to be 
available as an output after the event finishes executing. 
Any number of uniquely named event input parameters can be collected before firing an event. Upon 
firing the event, each is converted to an event parameter. 
event message 
A message, initiated by the event system, sent from one system user to another, that in many 
respects simulates an e-mail message. Event messages are created by event actions of a Notify or 
Prompt type, or by Inbox activities such as Forward, Reply, and Reply All, or from the Send 
Message form. 
Event messages can appear in the Sent Items folder of the sender, and the Inbox of each recipient. 
For more information, see ”Event Messages” on page 5-57. 
event output parameter 
A named static value passed from an event upon its finish. Any number of uniquely named event 
output parameters can be associated with an event. Each output is created from an event parameter 
marked for output. 
event parameter 
A named storage area retrievable by an event action, that is associated with an event that has been 
generated and is processing. The system creates event parameters from event input parameters 
when the event is generated. 
Event parameters can be set to be available to whatever process generated the event, after the event 
finishes. In this case, they can also be set by event actions and can result in the creation of event 
output parameters. 
event queue 
A FIFO list of events and event handlers to be processed asynchronously. Each entry has an 
associated user name, configuration name, and request date. 
event state 
1. A collection of data related to the current status of a running or finished event. This status is viewed 
using the Event Status form. 
2. An optional text string that displays on the Event Status form when the event reaches certain 
milestones or finishes executing successfully. This text string is defined by the event handler's 
creator and associated with the Achieve Milestone and Finish action types as a parameter. 
event trigger 
A condition that causes an event to be generated with optional parameters. 
For more information, see ”About event triggers” on page 3-34.

event variable 
A named storage area, the value of which can be set and retrieved by an event action associated with 
a running event handler. When associated with a synchronous event handler, an event variable can 
be designated as Persistent, in which case the value of the variable can be passed on to the next 
event handler. 
FIFO 
First In, First Out. 
framework 
The multi-tiered software structure that makes up the entire system. In this application, the framework 
consists of three basic tiers: 
z
The client tier, known as WinStudio. 
z
The middle tier 
z
The database tier 
For more information, see the "System Architecture" chapter in your System Administration Guide. 
framework event 
An event which has been designed to be generated only in reference to certain framework 
occurrences. 
initial variable 
A named static value for an event variable associated with an event handler. This value provides the 
initial value of the event variable when the event handler begins executing. 
Each event variable contains an authorization level that provides a default access within the scope of 
an event action that: 
z
Does not have a default access value defined on the Variable Access tab of the Event Actions 
form. In this case, default access value is determined on the Event Variable Groups form. 
z
Has a default access of Default on the Variable Access tab of the Event Actions form. 
metadata 

information about data formats that are interpreted during run time, rather than compiled code (also 
called "procedural code"). 
middle tier 
The layer of software in the database system which provides the connections between the client tier 
(WinStudio) and the database tier. The middle tier has two primary functions: 
z
To provide access from the client tier to the database through IDOs (Intelligent Data Objects). The 
client tier never communicates directly with the database. In this respect, the middle tier can be 
thought of rather like a telephone: It allows two parties to talk to one another, but not face-to-face. 
z
To receive form-rendering requests from the client tier, retrieve the appropriate form-rendering 
data from the forms database, and return that data to the client so that the form displays correctly. 
For more information about the middle tier, see the "System Architecture" chapter in your System 
Administration Guide.

synchronous event handler
An event handler designed to execute sequentially with other handlers, and whose triggering process 
blocks while waiting for it to finish (unless part of an event fired asynchronously). If any one event 
handler in the sequence fails, then the whole sequence fails. 
See also "asynchronous event handler." 
transactional events or event handlers 
One of a group of events or handlers that are included in a single transaction. Typically, all the event 
handlers and their actions must execute successfully before the transaction is considered finished 
and any results or data are committed. 
If any of the events or handlers in a transaction do not finish successfully, the entire transaction fails 
and all data and variable values roll back (revert) to their original values. 
WinStudio 
The client software in the database system, sometimes referred to as the "presentation layer," 
through which users interact with information in the database. WinStudio displays forms and provides 
the interface through which users can find, add, edit, sort, and delete data. 
For more information, see the "System Architecture" chapter in your System Administration Guide.

Index
A
Access As
form 3-31
identifier 3-31
action types B-126
actions
adjourning 2-21
for events 3-37
parameters B-126
types B-126
adjourning actions 2-21
adjournment 2-21
application event system
advantages of 1-9
design forms 3-43
elements 3-31
examples of use 1-10
flow diagram F-187
how it works 2-13
overview 1-7
Application events B-125
application-specific events 3-32
asynchronous
event handlers 2-16
events 2-17
events in transactions 2-26
authorization group for event system forms 3-43, 
4-53
B
BodOnReceive B-122
Boolean rules for expressions C-135
C
Caption, in Inbox form 5-59
complex expansions of functions B-127
ConditionalPlurality voting rule 5-63
constants, event global 3-42
controlling
ownership of metadata 3-31
sequence
event actions 2-14, 3-48
event handlers 2-14, 3-47
core (framework) events B-122
Core events 3-32
creating
event actions 3-37
event global constants 3-42
event handlers 3-36
event triggers 3-34
events 3-33
custom events and handlers 3-31– 3-51
designing custom events 3-46
setting up 3-45
customer-defined events 3-32
D
date expressions, rules C-146
defining
event actions 3-37
event global constants 3-42
event handlers 3-36
event triggers 3-34
events 3-33
design forms 3-43

Access As 3-31
authorization group for 3-43
Event Actions 3-37
Event Global Constants 3-42
Event Handlers 3-36
Events 3-32
location 3-43
designing custom events and handlers 3-31– 3-51
disabling event handlers
individually 2-15
with Session Access As 2-15
E
EarliestResponse voting rule 5-64
elements of the application event system 3-31
enumerations C-154
event action parameter forms 3-40
event actions 3-37
controlling sequence 2-14
defining 3-37
parameters B-126
setting sequence order 3-48
Event Actions form 3-37
Event Global Constants form 3-42
Event Handler Revisions form 4-55
Event Handler Status form 4-54
event handlers 3-36
controlling sequence 2-14
defining 3-36
designing custom 3-46
disabling individually 2-15
disabling with Session Access As 2-15
restricting which run 2-14
revisions 2-28
setting sequence order 3-47
setting up custom 3-45
status of
Failure 2-22
Success 2-21
success, failure, and retries 2-21
suspending 2-18
synchronicity (summary) B-121
synchronous and asynchronous 2-16
transactional 2-25
Event Handlers form 3-36
event messages 5-57– 5-66
indeterminate voting results 5-65
prompts and responses 5-61
related forms 5-57
voting rules 5-62
event queue
Framework Event Service 2-27
processing order 2-27
Event Queue form 4-54
Event Revisions form 4-55
Event Status form 4-53
event triggers 3-34
defininig 3-34
retesting 3-35
setting conditions for 3-35
Event Triggers form 3-34
Event Variable Groups form 3-41
event variables 3-41
events 3-32
action types B-126
actions 3-37
asynchronous 2-17

defining 3-33
firing from tiers B-120
flow diagram 2-13
framework (core) B-122
global constants 3-42
handlers 3-36
handling 2-13
message-related forms 5-57
Inbox 5-57
Saved Messages 5-59
Send Message 5-60
naming 3-33
parameter forms 3-40
parameters 3-38
passing 3-40
setting values and variables 3-40
revisions 2-28
setting up custom 3-45
suspend-committing mode 2-19
suspending 2-18
suspend-validating mode 2-18
synchronicity (summary) B-121
synchronous 2-16
transactional 2-24
triggers 3-34
defining 3-34
examples 2-13
retesting 3-35
setting conditions for 3-35
types 3-32
variables 3-41
where they can be generated from 2-14
Events form 3-32
Exclude Blank Access As setting
(Session Access As form) 2-15
expansions for functions
complex B-127
nested B-128
simple B-127
expressions
functions
pre-parser B-127
standard B-126
grammar C-131– C-156
character sets C-133
enumerations C-154
rules C-134
start symbol C-132
terminals C-133
keyword paren lists C-154
numeric-castable C-135
operators B-128
rules
Boolean C-135
dates C-146
numeric C-143
restricted argurments C-154
strings C-140
rules for C-135
scalar C-135
typeless, rules C-138
F
Failure status, event handler 2-22
failures
causes 2-22
handling with stored procedures D-157

ignoring 2-22
FireGenericNotifySp A-116
firing events (from tiers) B-120
forms 3-33
Access As 3-31
design
authorization group for 3-43
Event Actions 3-37
Event Global Constants 3-42
Event Handlers 3-36
Event Triggers 3-34
Event Variable Groups 3-41
Events 3-32
location 3-43
Workflow Event Handler Activation 3-44
event action parameters 3-40
message-related 5-57
Inbox 5-57
Saved Messages 5-59
Send Message 5-60
status
authorization group for 4-53
Event Handler Revisions 4-55
Event Handler Status 4-54
Event Queue 4-54
Event Revisions 4-55
Event Status 4-53
location 4-53
Framework Event Service 2-27
administering 2-28
processing order 2-27
setting up 2-27
framework events 3-32, B-122
functions B-126
complex expansions B-127
for expressions
pre-parser B-127
standard B-126
nested expansions B-128
simple expansions B-127
G
GenericNotify B-125
GenericNotify event A-116
GenericNotifyWithAttachments B-125
GenericSendEmail B-125
GenericSendPulseAlertBOD B-125
global constants 3-42
grammar for expressions C-131– C-156
character set C-133
enumerations C-154
rules C-134
Boolean C-135
dates C-146
expressions C-135
keyword paren lists C-154
numeric C-143
restricted arguments C-154
string C-140
typeless C-138
variable, constant, and event parameter 
references C-134
start symbol C-132
terminals C-133
H
handlers 3-36
Handlers, retrying 2-23

handling events 2-13
hierarchy of metadata (inherent) E-160
I
IdoOnInvoke B-123
IdoOnItemDelete B-123
IdoOnItemInsert B-123
IdoOnItemUpdate B-123
IdoOnLoadCollection B-122
IdoOnPersistFailed B-123
IdoOnUpdateCollection B-123
IdoPostInvoke B-123
IdoPostItemDelete B-123
IdoPostItemInsert B-123
IdoPostItemUpdate B-123
IdoPostLoadCollection B-122
IdoPostUpdateCollection B-123
ignoring failures 2-22
Inbox
form 5-57
indeterminate voting results for prompts 5-65
Initial Action field 3-48
initial states (variables) 3-41
integrating metadata from several sources E-
159– E-185
detailed examples E-161
using non-specific chronology E-165
using specific chronology E-162
inherent hierarchy of metadata E-160
maintaining handler IDs through updates E-

obsolete handlers E-182
overriding others’ handlers E-177
disabling E-182
exclusively E-180
non-exclusively E-178
overview and rationale E-159
performing upgrades E-173
protecting events from changes E-161
Interpret contents, attributes 5-59
K
Keep With fields 3-47
keywords
paren lists C-154
L
location
design forms 3-43
status forms 4-53
M
Majority voting rule 5-63
message-related forms 5-57
Inbox 5-57
Saved Messages 5-59
Send Message 5-60
messages (event) 5-57– 5-66
metadata
inherent hierarchy E-160
synchronizing E-159– E-185
MinimumCount voting rule 5-64
MinimumCountPreferredChoice voting rule 5-65
MinimumPercentage voting rule 5-64
MinimumPercentagePreferredChoice voting rule 
5-65
N
naming events 3-33
nested expansions of functions B-128
numeric expressions, rules C-143
numeric-castable expressions C-135

O
obsolete handlers E-182
operators for expressions B-128
P
parameters
for event actions B-126
passing 3-40, D-157
setting value and variables 3-40
syntax for 3-38
paren lists for keywords C-154
performing upgrades, integrating metadata E-173
Plurality voting rule 5-63
PreferredChoice voting rule 5-64
procedural code 1-9, -194
ProcessNewDataMaintenance B-125
prompts and responses 5-61
indeterminate voting results 5-65
voting rules 5-62
Q
queued events
Framework Event Service 2-27
processing order 2-27
Quorums 5-66
R
reference tables B-119– B-130
restricted arguments for expressions C-154
restricting which handlers run 2-14
resumption of adjourned events 2-21
retesting event triggers 3-35
Retrying event handlers 2-23
retrying event handlers 2-21
revisions, events and event handlers 2-28
rolling back transactions 2-26
rules
expression grammar
constant references C-134
dates C-146
event parameter references C-134
numeric C-143
restricted arguments C-154
strings C-140
typeless expressions C-138
variable references C-134
voting, prompts 5-62
S
samples
scenarios A-67–??
stored procedures D-157
Saved Messages form 5-59
scalar C-135
scalar expression expressions C-135
Scalar tuples C-139
scenarios, samples A-67–??
Send Message form 5-60
sequence
event actions 2-14, 3-48
event handlers 2-14, 3-47
Service Configuration Manager utility 2-27
Session Access As form 2-15
SessionOnLogin B-123
SessionOnLoginFailed B-124
SessionOnLogout B-124
SessionOnVarChanged B-124
SessionPostVarChanged B-124
setting
conditions for event triggers 3-35

sequence order
actions 3-48
handlers 3-47
variable and parameter values 3-40
simple expansions of functions B-127
status
event handlers
Failure 2-22
Success 2-21
forms
authorization group for 4-53
Event Handler Revisions 4-55
Event Handler Status 4-54
Event Queue 4-54
Event Revisions 4-55
Event Status 4-53
location 4-53
tracking 4-53– 4-55
stored procedures
calling synchronous events and handling fail-
ure D-157
passing parameters to a synchronous event D-

samples D-157
strings, rules C-140
Success event handler status 2-21
suspend-committing mode 2-19
suspend-validating mode 2-18
suspension 2-18– 2-20
event handlers 2-18
events 2-18
process for non-suspended events 2-20
process for suspended events 2-18
synchronicity 2-16– 2-17
event handlers (summary) B-121
events (summary) B-121
synchronization of metadata E-159– E-185
inherent hierarchy of metadata E-160
overview and rationale E-159
synchronous
calling events from stored procedures D-157
event handlers 2-16
events 2-16
events in transactions 2-24
syntax for event parameters 3-38
T
TaskListCheck B-125
ties in prompt votes 5-65
tracking status of events 4-53– 4-55
transactional
event handlers 2-25
events 2-24
transactions 2-24– 2-26
rolling back 2-26
with asynchronous events 2-26
with synchronous events 2-24
translatable captions 5-59
triggers for events 3-34
defining 3-34
examples 2-13
retesting 3-35
setting conditions for 3-35
types of events 3-32
U
upgrades, integrating metadata through E-173
V
variables

for events 3-41
setting parameter values 3-40
voting results indeterminate for prompts 5-65
voting rules for prompts 5-62
ConditionalPlurality 5-63
EarliestResponse 5-64
Majority 5-63
MinimumCount 5-64
MinimumCountPreferredChoice 5-65
MinimumPercentage 5-64
MinimumPercentagePreferredChoice 5-65
Plurality 5-63
PreferredChoice 5-64
W
Wait for Quorum 5-66
where events can be named 3-33
Workflow Event Handler Activation form 3-44
Workflow event handlers 1-12
