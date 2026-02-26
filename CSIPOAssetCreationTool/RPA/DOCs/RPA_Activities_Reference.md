# Infor RPA Studio - Activities Reference Guide

**Version**: Release 2026.x
**Purpose**: Quick reference for building RPA workflows in Infor RPA Studio

---

## Table of Contents

1. [Common Properties](#common-properties)
2. [Activity Catalog](#activity-catalog)
   - [Desktop](#desktop)
   - [Email](#email)
   - [Excel](#excel)
   - [Excel Online](#excel-online)
   - [Flowchart](#flowchart)
   - [HTTPS](#https)
   - [IONAPI](#ionapi)
   - [OCR](#ocr)
   - [OneDrive](#onedrive)
   - [PDF](#pdf)
   - [Primitives](#primitives)
   - [Programming](#programming)
   - [SharePoint List](#sharepoint-list)
   - [State Machine](#state-machine)
   - [System](#system)
   - [Two Factor Authentication](#two-factor-authentication)
   - [Web](#web)
   - [Workflow](#workflow)
3. [Error Handling](#error-handling)
4. [Variables and Arguments](#variables-and-arguments)
5. [Best Practices](#best-practices)
6. [Common Troubleshooting](#common-troubleshooting)

---

## Common Properties

Most activities share these common properties:

| Property | Data Type | Description |
|----------|-----------|-------------|
| Continue on Error | Boolean | Continue RPA flow even if activity fails (default: True) |
| Wait After | Int32 | Delay in seconds after activity completes |
| Wait Before | Int32 | Delay in seconds before activity runs |
| Response Code | Int32 | Activity result code |
| Display Name | String | Activity display name for identification |

### Response Code Values

| Code Range | Meaning |
|------------|---------|
| 200-290 | Success - valid output |
| 400-499 | Client error |
| 500-599 | Server error |

---

## Activity Catalog

### Desktop

Desktop activities automate interactions with Windows desktop applications.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| Click | Click desktop UI element | Element, ClickType |
| Double Click | Double-click element | Element |
| Get Text | Extract text from element | Element, Output: Text |
| Set Text | Input text into element | Element, Text |
| Send Hotkey | Send keyboard shortcuts | Key combination |
| Take Screenshot | Capture screen/element | FilePath, Element (optional) |

### Email

#### SMTP Activities

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Send SMTP Email** | Send email via SMTP | Recipient, Sender, Email Body, Email Subject, Attachments (List<String>), Server, Port, Password, Secure Connection |

#### Graph Email Activities (Microsoft 365)

**Note**: Requires OAuth Provider configuration for MS Graph in RPA Management.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Delete Outlook Graph Email** | Delete email messages | Mail Item (Office365Message), Delete Permanently (Boolean), Account (shared mailbox) |
| **Download Outlook Graph Email Attachment** | Download email attachments | Email (Office365Message), Attachment Filter, Save Destination, Output: File Paths (List<String>) |
| **Forward Outlook Graph Email** | Forward emails | Email (Office365Message), To, CC, BCC, Email Body, Attachments |
| **Get Outlook Graph Emails** | Retrieve emails from mailbox | Filter, Mail Folder Name, Mark as Read, Retrieve Top N, Retrieve Unread Only, Include Attachments, Output: Email List (Office365Message), Total Email Count |
| **Get Graph Mail by ID** | Retrieve email by MailID | Mail ID, Include Attachments, Account |
| **Mark Outlook Graph Email as Read/Unread** | Change read status | Email (Mail), Mark as Read (checkbox) |
| **Move Outlook Graph Email** | Move email to folder | Email (Office365Message), Destination Folder, Output: Moved Status, Moved Email |
| **Reply to Outlook Graph Email** | Reply to email | Email (Office365Message), To, CC, BCC, Email Body, Reply All |
| **Send Outlook Graph Email** | Send email via Outlook | To, CC, BCC, Email Body, Email Subject, Attachments, Save as Draft, Account |

### Excel

Excel activities for local workbook manipulation.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Add Sheet** | Add worksheet to workbook | Workbook Path, Worksheet Name |
| **Copy Sheet** | Copy worksheet | From Workbook, From Worksheet, To Workbook, To Worksheet |
| **Create Workbook** | Create new workbook | Workbook Path |
| **Delete Range** | Delete cell range | Workbook Path, Worksheet Name, Range, Shift (None/Up/Left) |
| **Read Cell** | Read single cell value | Workbook Path, Worksheet Name, Cell Address, Formula (Boolean), Output: Cell Value |
| **Read Column** | Read column values | Workbook Path, Worksheet Name, Column Number, Output: Results (Object[]) |
| **Read CSV** | Read CSV file | Filename, Has Headers, Delimiter, Output: Data Table |
| **Read Range** | Read cell range | Workbook Path, Worksheet Name, Range, Output: Data Table |
| **Read Row** | Read row values | Workbook Path, Worksheet Name, Row Number, Output: Result (Object[]) |
| **Rename Sheet** | Rename worksheet | Workbook Path, Original Worksheet Name, New Worksheet Name |
| **Write Cell** | Write to single cell | Workbook Path, Worksheet Name, Cell Address, Cell Value |
| **Write Range** | Write data table to range | Workbook Path, Worksheet Name, Data Table, Starting Cell, Has Headers |

**Range Notation**: Use A1-style notation (e.g., "A1:B5", "A1", "Sheet1")

### Excel Online

Excel Online activities for Microsoft 365 workbooks via Graph API.

**Prerequisite**: Authorize MS Graph OAuth Provider in RPA Management.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Add Sheet** | Add worksheet | Workbook (OneDriveItem), Worksheet Name |
| **Create Workbook** | Create new workbook | Workbook Name, Folder, First Sheet Name, Output: Workbook (OneDriveItem) |
| **Delete Columns** | Delete columns | Workbook, Worksheet Name, Range |
| **Delete Range** | Delete cell range | Workbook, Worksheet Name, Range |
| **Delete Rows** | Delete rows | Workbook, Worksheet Name, Range |
| **Delete Sheet** | Delete worksheet | Workbook, Worksheet Name |
| **Read Cell** | Read cell value | Workbook, Worksheet Name, Cell Address, Output: Cell Value, Formula |
| **Read Range** | Read cell range | Workbook, Worksheet Name, Range, Output: Data Table |
| **Rename Sheet** | Rename worksheet | Workbook, Worksheet Name, New Worksheet Name |
| **Write Cell** | Write cell value | Workbook, Worksheet Name, Cell Address, Cell Value |
| **Write Column** | Write column data | Workbook, Worksheet Name, Data Table, Range |
| **Write Range** | Write data table | Workbook, Worksheet Name, Data Table, Range |
| **Write Row** | Write row data | Workbook, Worksheet Name, Data Table, Range |

### Flowchart

Activities for creating flowchart-based workflows.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Flowchart** | Container for flowchart activities | - |
| **Flow Decision** | Branch based on condition | Condition (Boolean), TrueLabel, FalseLabel |
| **Flow Switch** | Multi-branch switch | Expression, Case values |

### HTTPS

Generic HTTP request activity for external APIs.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **HTTPS Request** | HTTP request to any API | Method (GET/POST/PUT/DELETE), URL, Content Type, Headers (List<String>), Query Parameters (List<String>), POST Data (Object), File Attachments (List<String>), Output: Response (ResponseObject), Status Code |

**Content Types**: application_json, application_xml, text_plain, text_xml, multipart_formdata, application_x_www_form_urlencoded

**Response Formats**:
- `ResponseObject.ReadAsText()` - Text format
- `ResponseObject.ReadAsJson()` - JToken format
- `ResponseObject.ReadAsXml()` - XmlDocument format

### IONAPI

API requests to the current tenant's API Gateway.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **IONAPI Request** | Request to tenant API Gateway | Method, URL, Content Type, Headers, Query Parameters, POST Data, File Attachments, Output: Response (ResponseObject), Status Code |

**Note**: Only validates APIs available under the current logged-in tenant.

### OCR

Optical Character Recognition activities.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Extract Data** | Extract data from document | Document Path, Output: Response (JToken) |
| **Extract Document Key-Values** | Extract specific keys | OCR Document, List of Keys (List<String>), Pages, Formatted Output, Execute, Output: Response (JToken) |
| **Extract Table** | Extract tables using regex | File Path, Page No, Start Regex, End Regex, Has Header, Execute, Output: Response (JToken) |
| **Get OCR Text** | Extract text from document | FilePath, Pages, Execute, Output: Response (JToken) |
| **Get OCR Result by JobID** | Get results for submitted job | JobID, Output: OCR Response (JToken) |
| **Submit OCR Job** | Submit document for OCR | Document Path, OCR Provider Name, Model Name, IDP Flow Name, Pages, Output: JobID |

**Extraction Methods**:
1. **Regular Expression Based**: Pattern matching on OCR text (most accurate)
2. **Layout Based**: Template-based extraction with visual mapping
3. **Flow Based**: IDP service flows for document classification

**Supported Formats**: jpg, jpeg, png, pdf

### OneDrive

OneDrive and SharePoint file operations via Microsoft Graph.

**Prerequisite**: Authorize MS Graph OAuth Provider in RPA Management.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Copy File/Folder** | Copy item | File or Folder to Copy (OneDriveItem), Target Folder (OneDriveItem), New Name, Account |
| **Create Folder** | Create folder | Folder Name, Target Folder (OneDriveItem), Account |
| **Delete File/Folder** | Delete item | File or Folder to Delete (OneDriveItem), Account |
| **Download File** | Download to local | File to Download (OneDriveItem), Download Location, Account |
| **Export File as PDF** | Convert and export as PDF | File to Export (OneDriveItem), Download as File, Account |
| **Find Files and Folders** | Search items | Query, Subfolder, Site URL (SharePoint), Drive Name, Account, Output: Item (OneDriveItem), Results (OneDriveItem[]) |
| **For Each Files or Folder** | Iterate items | Search Keyword, Folder, Return Item (files/folders/both), Limit Returns, Account, Output: Result (String[]) |
| **Get Files/Folder** | Get item by ID/URL | OneDriveItem Id, OneDriveItem URL, Site URL, Drive Name, Account, Output: Item (OneDriveItem) |
| **Move File/Folder** | Move item | File or Folder to Move (OneDriveItem), Destination Folder (OneDriveItem), New Name, Account |
| **Share File/Folder** | Share with recipients | File or Folder to Share (OneDriveItem), Grantee Type, Grantee Permission (View/Edit), Recipients, Message, Output: Access URL |
| **Upload File** | Upload local file | File to Upload, Destination Folder (OneDriveItem), In Case of Conflict (Replace/Fail/Rename), Account |

### PDF

PDF document manipulation activities.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Extract PDF Images** | Extract images from PDF | File Path, Image Format (Jpeg/Png), Output File Path |
| **Extract PDF Text** | Extract text from PDF | File Path, Page Range, Output: Extracted Text |
| **Merge PDF Documents** | Merge multiple PDFs | Input Files (List<String>), Target File Name, Target File Path, Output: Output File |
| **Retrieve PDF Page Count** | Get page count | File Path, Output: Pages (Int32) |
| **Split PDF Documents** | Split PDF | File Path, Output Directory, Split Criteria (Page Number/Size), Page Selection, Split Size |

### Primitives

Basic workflow activities.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Assign** | Assign value to variable | To (variable name), Value |
| **Delay** | Pause execution | Duration (TimeSpan, format: hh:mm:ss) |

### Programming

Data manipulation and scripting activities.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Add DataTable Column** | Add column to DataTable | DataTable, Column Name, Type, Column (DataColumn), Options: Allow Null, Auto Increment, Default Value, Max Length, Unique |
| **Add DataTable Row** | Add row to DataTable | DataTable, Array Row (Object[]) or Data Row |
| **Build Data Table** | Create new DataTable | Output: Data Table |
| **Delete DataTable Column** | Delete column | DataTable, Column Name or Index or Column (DataColumn) |
| **Delete DataTable Row** | Delete row | DataTable, Index or DataRow |
| **Invoke Method** | Run public method | Target Object/Type, Method Name, Parameters, Generic Type Argument, RunAsynchronously, Output: Result |
| **Invoke Python Script** | Execute Python script | Script Location, Additional Arguments, Python Installation, Requirements, Script Timeout, Output: Python Output, Python Error Output, Package Installation Errors |
| **Try Catch** | Exception handling | Try (activities), Catch (exception handlers), Finally (always runs) |

### SharePoint List

SharePoint List manipulation via Microsoft Graph.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Add List Items** | Add items to list | List (SharePointList), List Item (DataTable), Output: List Items (SharePointListItem[]) |
| **Delete List Item** | Delete list item | List Item (SharePointListItem) |
| **Get Individual List Items** | Convert list to array | List (SharePointList), Output: Individual List Items (SharePointListItem[]) |
| **Get List Information** | Get list metadata | List Name or ID, Site URL or ID, Include Column Definitions, Output: List (SharePointList) |
| **Get List Items** | Retrieve list items | List (SharePointList), Columns to Retrieve, Output: List Items (DataTable) |
| **Update List Item** | Update item properties | List Item (SharePointListItem), Update Item (DataTable) |

### State Machine

Event-driven workflow modeling.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **State Machine** | Container for states | Display Name |
| **State** | Workflow state | Entry (activities), Exit (activities), Transition (to other states) |
| **FinalState** | End state | Entry (activities) |

### System

File system and system-level activities.

#### File Operations

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Append Line** | Append text to file | Source Filepath, Line |
| **Copy File** | Copy file | Source Filepath, Target Directory, Target Name |
| **Create File** | Create empty file | Target Filepath, Target Filename |
| **Delete File** | Delete file | Target Filepath |
| **Move File** | Move file | Source Filepath, Target Filepath, Target Filename |
| **Path Exists** | Check if path exists | Path, Output: Is Valid (Boolean) |
| **Read Lines of File** | Read file lines | Source Filepath, Output: Lines (List<String>) |
| **Read Text File** | Read entire file | Source Filepath, Output: Text |
| **Write Text File** | Write lines to file | Source Filepath, Lines (List<String>) |
| **Get Files in Directory** | List files | Path, File Type (filter), Include Subdirectories, Output: Files (List<String>) |
| **Get File Size** | Get file size in KB | File Path, Output: Size (Int32) |

#### Directory Operations

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Compress Directory** | Compress directory | Source Filepath, Target Directory, Target Name, Password |
| **Copy Directory** | Copy directory | Source Filepath, Target Directory, Target Name |
| **Create Directory** | Create directory | Target Directory, Target Name |
| **Delete Directory** | Delete directory | Source |
| **Extract Directory** | Extract zip file | Source, Target, Password |
| **Get Directories** | List directories | Path, Include Subdirectories, Output: Directories |
| **Move Directory** | Move directory | Source Filepath, Target Directory, Target Name, Overwrite Directory |

#### FTP Operations

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **FTP File Download** | Download from FTP | Host, Port#, Protocol (FTP/SFTP), Remote File Full Path, File Path, Username, Password, Transfer Mode (ASCII/Binary), Timeout |
| **FTP File Upload** | Upload to FTP | Host, Port#, Protocol, File Path, Remote Directory, Remote File Name, Username, Password, Transfer Mode, Retry Attempts, Timeout |
| **FTP File Delete** | Delete from FTP | Host, Port#, Protocol, File Name, File Path, Username, Password, Timeout |
| **FTP File Move** | Move on FTP | Host, Port#, Protocol, File Name, Source, Target, Username, Password, Timeout |
| **FTP List Directory** | List FTP directory | Host, Port#, Protocol, Remote Directory Full Path, Username, Password, Timeout, Output: Retrieved Files, Retrieved Directories |

#### Data Transformation

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Deserialize JSON** | JSON string to JToken | JToken String, Output: JToken Object |
| **Serialize JSON** | JToken to JSON string | JToken Input, Output: JToken String |
| **JQ Transform** | Filter JSON with JQ | JSON Input (List<String>), Filter (JQ expression), Raw Output, Output: JSON Output (JToken) |
| **JSON to DataTable** | Convert JSON array to DataTable | JSON Array (JToken), Output: DataTable |
| **File to Base64 String** | Encode file to Base64 | Filepath, Output: Base64 String |
| **Data Compression** | Compress text data | File Path, Base64 Encode, Output: Destination Path |

#### Environment & Utilities

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Get Environment Variable** | Get env variable value | Name, Output: Value |
| **Get Environment Variable List** | Get all env variables | Output: Environment Variables (Dictionary<String,String>) |
| **Set Environment Variable** | Set env variable | Name, Value |
| **Download File by URL** | Download file from URL | URL, Target, Name, Async |
| **Message Box** | Display message | Input Text, Message Box Title, Message Box Type (OK/OKCancel/YesNo/YesNoCancel), Output: Button Selection |
| **Templating Activity** | Complete template | Template, Values (List<String>), Output: Text |
| **Write Line** | Print to output panel | Line |
| **User Input Prompt** | Prompt for user input | Prompt Message, Prompt Title, Input Type, Options, Timeout, Default Value |
| **Log Execution Message** | Log custom message | Message, LogType (Info/Warning/Error/Summary), SectionName, Output: Job Instance ID |

### Two Factor Authentication

MFA code generation activities.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Get Microsoft OTP Code** | Generate Microsoft MFA code | Secret Key, Output: OTPCode |
| **Get Google OTP Code** | Generate Google MFA code | Secret Key, Output: OTPCode |

**Usage Notes**:
- Secret key is generated when enrolling a device for 2FA
- For Infor tenants with TOTP enabled, use Get Microsoft OTP Code

### Web

Browser automation activities.

**Prerequisite**: Must have Open Browser activity with valid URL before adding web activities.

#### Browser Control

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Open Browser** | Open browser with URL | URL, Browser Type (Chrome/Edge), Private Browsing Enabled, Zoom Percentage |
| **Close Browser** | Close browser | - |
| **Close Tab** | Close current tab | - |
| **Navigate To** | Navigate to URL | URL, Zoom Percentage |
| **New Tab** | Open new tab | URL |
| **Switch Tab** | Switch to tab | Tab Index or Window Handle |
| **Go Back** | Navigate back | - |
| **Go Forward** | Navigate forward | - |
| **Refresh Browser** | Refresh page | - |
| **Maximize Window** | Maximize browser | - |
| **Minimize Window** | Minimize browser | - |

#### Element Interaction

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Click** | Click element | Web Element (WebElementItem), XPath, Frames (List<String>) |
| **Right Click** | Right-click element | Web Element, XPath, Frames |
| **Check** | Check/uncheck checkbox | Web Element, XPath, Frames, Action (Check/Uncheck) |
| **Set Text** | Enter text in element | Web Element, XPath, Frames, Text, Clear Text (Boolean) |
| **Add Date** | Add date to element | Web Element, XPath, Frames, Date Value, Date Format (dd/MM/yyyy or MM/dd/yyyy), Clear Text |
| **Select Dropdown Item** | Select dropdown option | Web Element, XPath, Frames, Item (value/text) |
| **Select Multiple Items** | Multi-select | Web Element, XPath, Frames, Items |
| **Send Hotkey** | Send keyboard shortcut | Key combination |
| **File Upload** | Upload file | File Path, WindowName |

#### Data Extraction

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Get Element Text** | Extract element text | Web Element, XPath, Frames, Output: Element Value |
| **Get Page Text** | Extract page text | Frames, Output: Page Text |
| **Get Table** | Extract table as DataTable | Web Element, XPath, Frames, Include Headers, Output: Data Table |
| **Get Attribute** | Get element attribute | Web Element, XPath, Frames, Attribute Name, Output: Result |
| **Find Elements** | Find child elements | XPath, Frames, Output: Elements (List<WebElementItem>) |
| **Element Exists** | Check if element exists | Element (XPath), Frames, Output: Is Found (Boolean) |

#### Screenshots & PDF

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Take Screenshot** | Capture screenshot | File Path, Element (optional) |
| **Save As PDF** | Save page as PDF | File Path |
| **Save Image** | Save element as image | Web Element, File Path |

#### Frame & Shadow DOM

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **To IFrame** | Switch to iframe | XPath, Frames |
| **Switch to Default** | Switch to default content | - |
| **To Shadow Root** | Access shadow DOM | Web Element, XPath |

### Workflow

Control flow and workflow management activities.

| Activity | Purpose | Key Properties |
|----------|---------|----------------|
| **Sequence** | Container for sequential activities | Activities |
| **If** | Conditional branching | Condition (Boolean), Then, Else |
| **Switch** | Multi-case branching | Expression, Cases, Default |
| **While** | Loop while condition true | Condition (Boolean), Body |
| **Do While** | Loop at least once | Condition (Boolean), Body |
| **For Each** | Iterate over collection | TypeArgument, Values (List<T>), Body |
| **Parallel** | Run activities in parallel | Branches |
| **Pick** | Wait for first trigger | Branches (PickBranch) |
| **Pick Branch** | Branch within Pick | Trigger, Action |
| **Invoke Workflow** | Call sub-workflow | WorkflowFile, InputArguments (Dictionary<String,Object>), OutputArguments (IDictionary<String,Object>) |
| **Terminate Workflow** | End workflow | Exception, Reason |
| **Throw** | Throw exception | Exception (with message) |
| **Rethrow** | Re-throw caught exception | - (only in Catch block) |

---

## Error Handling

### Try-Catch Pattern

The Try-Catch activity handles exceptions in workflows:

```
Try
  └── Activities that may throw exceptions
Catch
  └── System.Exception (or specific exception type)
      └── Error handling activities
Finally
  └── Cleanup activities (always runs)
```

### Common Exception Classes

| Exception | Use Case |
|-----------|----------|
| System.Exception | Catch all exceptions |
| System.IO.IOException | File/directory operations |
| System.Net.WebException | Network/HTTP errors |
| WebElementNotFoundException | Web element not found |
| System.TimeoutException | Operation timeout |
| System.ArgumentException | Invalid arguments |

### Continue on Error Property

Most activities have a "Continue on Error" property:
- **True** (default): Workflow continues even if activity fails
- **False**: Exception is thrown, can be caught by Try-Catch

### Error Handling Best Practice

```
1. Use ContinueOnError="True" for recoverable operations
2. Check Response Code after activity execution
3. Use If activity to handle based on Response Code
4. For critical operations, use Try-Catch with ContinueOnError="False"
```

### Throw and Rethrow

- **Throw**: Create and throw a new exception with custom message
- **Rethrow**: Re-throw the exception caught in a Catch block (preserves stack trace)

---

## Variables and Arguments

### Data Types

| Type | Description | Example |
|------|-------------|---------|
| String | Text values | "Hello World" |
| Int32 | Integer numbers | 42 |
| Boolean | True/False | True, False |
| DataTable | Tabular data | Excel/CSV data |
| List<T> | Collection of items | List<String>, List<Int32> |
| Dictionary<K,V> | Key-value pairs | Dictionary<String,Object> |
| JToken | JSON data | JSON responses |
| DateTime | Date and time | DateTime.Now |
| TimeSpan | Duration | 00:05:00 |
| Object | Any type | General purpose |

### RPA-Specific Types

| Type | Description | Used In |
|------|-------------|---------|
| Mail / Office365Message | Email object | Graph Email activities |
| WebElementItem | Browser element | Web activities |
| ResponseObject | HTTP response | HTTPS/IONAPI activities |
| OneDriveItem | File/folder reference | OneDrive activities |
| SharePointList | SharePoint list | SharePoint activities |
| SharePointListItem | List item | SharePoint activities |
| DataRow | Table row | DataTable operations |
| DataColumn | Table column | DataTable operations |

### Variable Scope

- **Sequence/Container Level**: Available within container and child containers
- **Workflow Level**: Available throughout the workflow
- **Arguments**: Pass data between workflows (In/Out/In-Out)

### Global Arguments

- Must be prefixed with "GLOBAL_"
- Defined in RPA Management
- Available across all workflow executions
- Used for environment-specific configuration

### Argument Directions

| Direction | Description |
|-----------|-------------|
| In | Input to sub-workflow |
| Out | Output from sub-workflow |
| In/Out | Both input and output |

### Invoke Workflow Arguments

```
InputArguments: Dictionary<String, Object>
  - Pass values to sub-workflow

OutputArguments: IDictionary<String, Object>
  - Receive values from sub-workflow
  - Extract: CType(outputDict("key"), TargetType)
```

---

## Best Practices

### Attended Mode (Human Interaction)

1. **User Prompts**: Use User Input Prompt for required user input
2. **Message Boxes**: Provide feedback and confirmation dialogs
3. **Error Display**: Show meaningful error messages to users
4. **Timeout Handling**: Set appropriate timeouts with default values
5. **Visual Feedback**: Use progress indicators for long operations

### Unattended Mode (Server Execution)

1. **No UI Dependencies**: Avoid Message Box, User Input activities
2. **Robust Error Handling**: Implement comprehensive Try-Catch blocks
3. **Logging**: Use Log Execution Message for audit trails
4. **Email Notifications**: Send error/completion notifications
5. **Retry Logic**: Implement retries for transient failures
6. **Session Management**: Handle RDP session requirements

### Server Recommendations for Unattended Mode

- Disable interactive logon messages
- Configure RPA Robot Service for auto-start
- Verify Windows user is in RDP user group
- Ensure password hasn't expired
- Check domain settings match between device and robot

### General Best Practices

#### XPath and Selectors

1. **Use Stable Selectors**: Prefer ID and name attributes over position-based selectors
2. **Avoid Brittle Paths**: Don't rely on exact element positions
3. **Handle Dynamic Elements**: Use contains(), starts-with() functions
4. **Test Selectors**: Verify XPath in browser developer tools

#### Workflow Design

1. **Modular Design**: Break workflows into reusable sub-workflows
2. **Configuration Variables**: Externalize environment-specific values
3. **Meaningful Names**: Use descriptive activity display names
4. **Documentation**: Add comments via display names
5. **Version Control**: Track changes in source control

#### Performance

1. **Minimize Waits**: Use element detection instead of fixed delays
2. **Batch Operations**: Process data in batches when possible
3. **Close Resources**: Close browsers, files after use
4. **Efficient Loops**: Minimize activities inside loops

---

## Common Troubleshooting

### RPA Studio Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Activity could not be loaded | Invalid XAML syntax | Check for XML comments (not supported), verify ViewStateData entries |
| Value not supplied error | Missing required argument | Ensure all required properties are set |
| Element not found | XPath incorrect or element not loaded | Add wait, verify XPath, check frames |
| File already exists (404) | Create File with existing name | Check file existence first with Path Exists |
| File not found (404) | Write Text File to non-existent file | Create file first |

### Web Automation Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Element not clickable | Element hidden or overlapped | Scroll element into view, add wait |
| Timeout waiting for element | Page not fully loaded | Increase wait time, use Element Exists |
| Frame not accessible | Not switched to iframe | Use To IFrame activity first |
| Stale element reference | Page refreshed | Re-find element after page changes |

### API/Integration Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Check OAuth configuration, refresh token |
| 403 Forbidden | Insufficient permissions | Verify service account roles |
| 404 Not Found | Wrong endpoint URL | Verify API endpoint path |
| 500 Server Error | Server-side issue | Check server logs, retry later |

### FTP Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Wrong host/port | Verify server address and port |
| Authentication failed | Wrong credentials | Check username/password |
| Permission denied | Insufficient FTP permissions | Verify user permissions on server |
| Timeout | Network/firewall issues | Check firewall rules, increase timeout |

### Unattended Execution Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Robot not logging on | Password expired/changed | Update robot password |
| Nothing happens after logon | Robot Service not configured | Configure auto-start in Task Scheduler |
| FreeRDP blocked | Antivirus false positive | Whitelist FreeRDP.exe |
| Domain mismatch | Robot/device domain different | Ensure exact domain match |

### Configuration Manager Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Unable to connect | Invalid IONAPI file | Re-download credentials with Create Service Account enabled |
| Missing RPA-ADMIN role | Service account not configured | Assign RPA-ADMIN IFS role to service account |

---

## Quick Reference: Response Code Handling

```
Response Code Check Pattern:
1. Execute activity
2. Check Response Code variable
3. If 200-290: Success - continue
4. If 400-499: Client error - check inputs
5. If 500-599: Server error - retry or alert
```

---

*Document generated from Infor Robotic Process Automation User Guide Release 2026.x*
