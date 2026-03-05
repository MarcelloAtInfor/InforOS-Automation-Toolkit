# Infor RPA Studio Repository - Architectural Guide

### CLAUDE.md
When the user confirms that changes or discoveries are good/correct, update this CLAUDE.md file with the new information. This ensures future Claude Code sessions have access to accumulated knowledge.

### log.md
Always update log.md to track project progress. Record completed steps, current status, new discoveries, and next steps. This serves as the running history of the project and helps maintain context across sessions.

## Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.** Infor OS is NOT a typical local development stack - there is no local runtime, domain knowledge gaps cause frequent errors, and only the user can validate results in the live environment. Do NOT batch multiple phases together. After each phase: summarize what was done, what needs testing, and WAIT for user confirmation before continuing. See root `CLAUDE.md` for full details.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Repository Overview

This is a multi-project Infor RPA Studio workspace containing 25+ automation workflows for business process automation. The repository focuses on document processing, invoice handling, email automation, and ERP integration workflows deployed across multiple Infor Cloud Suite tenants.

**Technology Stack:**
- **Platform**: Infor RPA Studio (proprietary RPA tool)
- **Workflow Definition**: XAML files with VBScript expressions
- **Integration Layer**: Infor ION API, Infor Document Management (IDM), Data Lake, Office 365
- **Deployment Model**: Multi-tenant Infor Cloud Suite environments

**Key Characteristic**: This is NOT a traditional code repository with source files and build scripts. It's a collection of workflow definitions that are executed by the Infor RPA Studio runtime.

## Working with RPA Studio

### Project Organization
- Each subdirectory represents a separate RPA project
- Projects are opened and edited in Infor RPA Studio IDE
- No compilation step - Studio validates and executes XAML workflows directly
- Testing is integration-based, not unit-test driven

### Development Workflow
1. Open project folder in RPA Studio
2. Edit main workflow XAML files
3. Configure parameters and connections
4. Test workflows against development tenant
5. Deploy to production tenant(s) via Studio or CI/CD

### No Traditional Build Process
- XAML workflows are interpreted, not compiled
- Dependencies are managed through Studio's package system
- Validation happens at design-time in Studio or runtime during execution

## Project Structure (Standard Pattern)

```
ProjectName/
├── project.json              # Project metadata and Studio configuration
├── Main.xaml                 # Entry point workflow
├── <SubWorkflow>.xaml        # Reusable sub-workflows
├── .local/                   # Local settings (not deployed)
├── .screenshots/             # UI activity screenshots for documentation
└── .tmh/                     # Temporary metadata files
```

### Key Files

**project.json**
- Defines project name, description, and entry point
- Lists RPA Studio package dependencies
- Specifies project type and framework version

**Main.xaml**
- Primary workflow entry point
- Contains configuration variables at top (Arguments/Variables sections)
- Orchestrates sub-workflow calls
- Implements main business logic flow

**Sub-workflow XAMLs**
- Reusable operations split into separate files
- Called via "Invoke Workflow File" activities
- Enable modular design and code reuse across projects

## Common Workflow Architecture

Most projects follow this standard pattern:

```
1. Configuration & Initialization
   ↓
2. Input Retrieval (email, file system, API)
   ↓
3. Data Extraction/Processing
   ↓
4. Backend Integration (ION API calls to ERP)
   ↓
5. File Organization (IDM upload, archival)
   ↓
6. Notifications (email results, error alerts)
   ↓
7. Cleanup & Logging
```

### Architecture Patterns

**Configuration-Driven Design**
- Centralized parameters in Main.xaml Arguments/Variables
- Feature flags for optional functionality
- Environment-specific settings (URLs, accounts, credentials)
- Parameters passed through to sub-workflows

**Reusable Sub-Workflows**
- Common operations extracted to separate XAML files
- Examples: file operations, email sending, API calls, error handling
- Promotes consistency across projects

**Error Handling Strategy**
- Try-Catch blocks around major operations
- Error logging to Data Lake or file system
- Email notifications on failures
- Retry logic for transient failures

## Integration Architecture

### Infor ION API Integration
- RESTful API calls to Infor Cloud Suite ERP systems
- Authentication via OAuth 2.0 tokens
- Common operations: Create invoices, query POs, update transactions
- Handles both CloudSuite Financials and CloudSuite Industrial

### Infor Document Management (IDM)
- Document upload via REST API
- Attachment to ERP entities (invoices, suppliers)
- Document retrieval and download
- Metadata management

### Data Lake Persistence
- CSV/Excel file writes for audit trails
- Stores processing logs and extracted data
- Accessible via file share or cloud storage
- Used for reporting and troubleshooting

### Office 365 Integration
- Email processing (Outlook/Exchange)
- Attachment extraction and handling
- Email notifications for workflow results
- Calendar and contact operations (some projects)

### GenAI Integration (Advanced Projects)
- HTTP API calls to GenAI extraction services
- JSON payload/response handling
- OCR and intelligent document processing
- Validation of extracted data

## Configuration Management

### Configuration Locations

1. **Main.xaml Variables/Arguments** (Primary)
   - Tenant-specific URLs and endpoints
   - Email accounts and recipient lists
   - Feature flags (EnableNotifications, ProcessAttachments, etc.)
   - Business rules (thresholds, date ranges)
   - File paths and naming conventions

2. **project.json** (Secondary)
   - Project metadata (name, version)
   - RPA Studio settings

3. **External Config Files** (Some Projects)
   - Excel/CSV files for lookup data
   - JSON files for complex configurations

### Multi-Environment Support
- Configuration variables allow same workflow to run across tenants
- Typical environments: Development, Test, Production
- Tenant-specific parameters injected at deployment time

## Multi-Tenant Deployment

### Tenant Metadata Pattern
Projects are deployed to multiple Infor Cloud Suite tenants. Tenant-specific configuration typically includes:

- **Tenant Base URLs**: Different per environment
- **ION API Endpoints**: Tenant-specific
- **Email Accounts**: Dedicated mailboxes per tenant
- **Data Lake Paths**: Segregated by tenant
- **Business Rules**: May vary by tenant (approval thresholds, etc.)

### Deployment Strategy
- Single workflow codebase
- Configuration injected per tenant
- Schedules managed in RPA Studio Server
- Monitoring and logging per tenant instance

## Notable Projects

### CSIInvoiceProcessingGenAIV2 (Reference Architecture)

The most sophisticated project in the repository, demonstrating advanced patterns:

**Complexity**: 30+ workflow files
**Key Features**:
- GenAI-powered data extraction from invoice PDFs
- Multi-PO matching and line-item distribution
- Complex business rule validation
- Comprehensive error handling and notifications
- Modular sub-workflow architecture

**Configuration**: 27+ parameters including:
- Tenant URLs (ION, IDM, Data Lake)
- Email accounts (inbox, error notifications)
- ERP type selection (Financials vs Industrial)
- Feature flags (enable notifications, testing mode, GenAI options)
- Business thresholds and date handling rules

**Architecture Highlights**:
- Main orchestration workflow delegates to specialized sub-workflows
- Reusable components for ION API calls, GenAI extraction, file handling
- State management across multi-step processing
- Robust retry and error recovery logic

Use this project as a reference for:
- Complex document processing workflows
- AI/ML integration patterns
- Multi-system integration (ERP + GenAI + IDM)
- Enterprise-grade error handling and logging
- Configuration-driven design at scale

## Development Guidelines

### When Modifying Workflows

1. **Understand Configuration First**: Review all Variables/Arguments before making changes
2. **Preserve Reusability**: Keep sub-workflows generic and parameterized
3. **Maintain Error Handling**: Ensure Try-Catch blocks remain comprehensive
4. **Test Across Tenants**: Validate changes work with different configurations
5. **Document Parameters**: Add comments to new configuration variables

### When Creating New Projects

1. **Start with a Template**: Copy structure from similar existing project
2. **Plan Sub-Workflows Early**: Identify reusable operations upfront
3. **Design for Configuration**: Externalize all environment-specific values
4. **Implement Logging**: Add comprehensive logging from the start
5. **Consider Multi-Tenant**: Design for deployment across multiple environments

### Common Pitfalls

- **Hardcoded Values**: Always use variables for paths, URLs, credentials
- **Missing Error Handling**: Every external call needs Try-Catch
- **Monolithic Workflows**: Break large workflows into reusable components
- **Poor Logging**: Log enough detail to troubleshoot in production
- **Credential Exposure**: Never commit credentials; use Studio's secure storage
- **Overuse of ContinueOnError**: See section below

### ContinueOnError Best Practices (CRITICAL)

`ContinueOnError="True"` can mask real failures and cause misleading logs. Use it carefully:

**KEEP ContinueOnError="True" for:**
- `Append_Line` - Logging shouldn't crash workflow
- `Path_Validate` - 404 is expected when checking if path exists
- `File_Delete` - Cleanup operations (ok to fail if file doesn't exist)
- Setup/initialization sub-workflows

**SET ContinueOnError="False" for:**
- `InvokeWorkflow` calls to critical sub-workflows (OCR, API calls, business logic)
- `IONAPIRequestWizard` - API calls should fail loudly
- `DocumentOC` / `ExtractDataActivity` - OCR operations
- `File_Move` - Critical file operations
- `Directory_GetFiles` - Need to know if files can't be retrieved

**Why this matters:**
With `ContinueOnError="True"` on critical operations, the workflow continues after failures and may report SUCCESS when it actually failed. This makes debugging extremely difficult because:
1. Project logs show SUCCESS
2. Runtime logs show the actual ERROR
3. Users think everything worked when it didn't

## XAML Syntax Rules (CRITICAL)

When writing XAML workflow files for Infor RPA Studio, these syntax rules MUST be followed:

### NO XML Comments (CRITICAL)

**RPA Studio does NOT support XML comments.** Using them causes "Activity could not be loaded" errors and prevents the workflow from loading.

```xml
<!-- WRONG - This WILL BREAK the workflow -->
<!-- Any comment here -->
<Assign DisplayName="My Activity" ... />

<!-- CORRECT - No comments, use DisplayName for documentation -->
<Assign DisplayName="Extract Filename - gets file name from full path" ... />
```

### File_Move Activity Requirements

The `File_Move` activity REQUIRES an `OutputFile` variable - you cannot use `{x:Null}`:

```xml
<!-- WRONG - Causes "Value for required argument 'OutputFile' was not supplied" -->
<ias:File_Move OutputFile="{x:Null}" ... />

<!-- CORRECT - Must capture output to a variable -->
<Sequence.Variables>
  <Variable x:TypeArguments="x:String" Name="moveFileOutput" />
</Sequence.Variables>
<ias:File_Move OutputFile="[moveFileOutput]" Source="[sourcePath]" Target="[targetFolder]" ... />
```

### VBScript Expression Syntax

All values in `<InArgument>` tags must use VBScript expression syntax with square brackets:

```xml
<!-- WRONG - Will cause "Value was not supplied" error -->
<InArgument x:TypeArguments="x:String"></InArgument>
<InArgument x:TypeArguments="x:String">PENDING</InArgument>

<!-- CORRECT - Use VBScript brackets -->
<InArgument x:TypeArguments="x:String">[""]</InArgument>
<InArgument x:TypeArguments="x:String">["PENDING"]</InArgument>
```

### VBScript Functions Not Available (CRITICAL)

RPA Studio uses VB.NET expressions, NOT VBScript. Several common VBScript constants and functions are **not available**:

```xml
<!-- WRONG - VBScript functions cause "not declared" errors -->
[vbLf]                    <!-- Line feed constant -->
[vbCr]                    <!-- Carriage return constant -->
[vbCrLf]                  <!-- CR+LF constant -->
[Chr(10)]                 <!-- Character function -->

<!-- CORRECT - Use .NET equivalents -->
[Convert.ToChar(10)]                        <!-- Line feed (LF) -->
[Convert.ToChar(13)]                        <!-- Carriage return (CR) -->
[System.Environment.NewLine]                <!-- Platform newline (CRLF on Windows) -->
```

**Common Conversions**:
| VBScript | .NET Equivalent |
|----------|-----------------|
| `vbLf` | `Convert.ToChar(10)` |
| `vbCr` | `Convert.ToChar(13)` |
| `vbCrLf` | `Convert.ToChar(13).ToString() + Convert.ToChar(10).ToString()` or `System.Environment.NewLine` |
| `Chr(n)` | `Convert.ToChar(n)` |
| `Asc(c)` | `Convert.ToInt32(c)` |

**Example - Splitting by Line Feed**:
```xml
<!-- WRONG -->
[text.Split(New Char() {Chr(10)}, StringSplitOptions.RemoveEmptyEntries)]

<!-- CORRECT -->
[text.Split(New Char() {Convert.ToChar(10)}, StringSplitOptions.RemoveEmptyEntries)]
```

### Type-Specific Examples

**Strings:**
```xml
<InArgument x:TypeArguments="x:String">[""]</InArgument>
<InArgument x:TypeArguments="x:String">["SUCCESS"]</InArgument>
<InArgument x:TypeArguments="x:String">[myVariable]</InArgument>
<InArgument x:TypeArguments="x:String">[myVariable + " text"]</InArgument>
```

**Integers:**
```xml
<InArgument x:TypeArguments="x:Int32">[0]</InArgument>
<InArgument x:TypeArguments="x:Int32">[500]</InArgument>
<InArgument x:TypeArguments="x:Int32">[count + 1]</InArgument>
```

**Booleans:**
```xml
<InArgument x:TypeArguments="x:Boolean">[True]</InArgument>
<InArgument x:TypeArguments="x:Boolean">[False]</InArgument>
<InArgument x:TypeArguments="x:Boolean">[myCondition]</InArgument>
```

### ViewStateData Entries (CRITICAL - Causes Load Errors)

Every activity with `sap2010:WorkflowViewState.IdRef` MUST have a matching `<sap2010:ViewStateData>` entry in the ViewStateManager section. Missing entries cause "Activity could not be loaded because of errors in the XAML" errors.

```xml
<!-- For each activity like this: -->
<Assign DisplayName="My Assign" sap2010:WorkflowViewState.IdRef="Assign_1">
  ...
</Assign>

<!-- You MUST have this in ViewStateManager at the end of the file: -->
<sap2010:ViewStateData Id="Assign_1" sap:VirtualizedContainerService.HintSize="564,60" />
```

**For Sequence containers**, add IsExpanded property:
```xml
<sap2010:ViewStateData Id="Sequence_1" sap:VirtualizedContainerService.HintSize="486,500">
  <sap:WorkflowViewStateService.ViewState>
    <scg:Dictionary x:TypeArguments="x:String, x:Object">
      <x:Boolean x:Key="IsExpanded">True</x:Boolean>
    </scg:Dictionary>
  </sap:WorkflowViewStateService.ViewState>
</sap2010:ViewStateData>
```

**HintSize Guidelines** (based on working files):
- Simple activities (Assign, Append_Line): `"564,60"` or `"512,60"`
- Inline activities (File_Move, GetFiles): `"564,22"` or `"512,22"`
- Sequence containers: `"486,500"` to `"634,1500"` depending on content
- If statements: `"512,700"` or similar
- ForEach/DoWhile loops: `"564,1350"` / `"582,762"`

### Argument Default Values (CRITICAL)

In RPA Studio, argument default values are set as **attributes on the Activity element**, NOT within `x:Members`.

**WRONG** (defaults won't appear in Arguments tray):
```xml
<Activity x:Class="RehostedWorkflowDesigner.Workflow" ...>
  <x:Members>
    <x:Property Name="configurationFolder" Type="InArgument(x:String)" />
  </x:Members>
```

**CORRECT** (defaults visible in Arguments tray):
```xml
<Activity x:Class="RehostedWorkflowDesigner.Workflow"
  this:Workflow.configurationFolder="C:\MyFolder"
  this:Workflow.pollingInterval="5"
  xmlns:this="clr-namespace:RehostedWorkflowDesigner"
  ...>
  <x:Members>
    <x:Property Name="configurationFolder" Type="InArgument(x:String)" />
    <x:Property Name="pollingInterval" Type="InArgument(x:Int32)" />
  </x:Members>
```

**Key Requirements**:
1. Add namespace: `xmlns:this="clr-namespace:RehostedWorkflowDesigner"`
2. Set defaults as attributes: `this:Workflow.argumentName="defaultValue"`
3. String values are plain text (not VBScript brackets)
4. Integer values are plain numbers
5. For VBScript expressions: `this:Workflow.path="[Environment.GetFolderPath(...)]"`

### Error Handling Patterns

#### Pattern 1: TryCatch Wrapper (Recommended for Sub-Workflows)

Use TryCatch to wrap entire sub-workflows for robust error handling. This ensures exceptions are caught, logged, and the workflow can set appropriate status output arguments.

```xml
<TryCatch DisplayName="TryCatch Main" sap2010:WorkflowViewState.IdRef="TryCatch_Main">
  <TryCatch.Variables>
    <!-- Variables scoped to TryCatch -->
  </TryCatch.Variables>
  <TryCatch.Try>
    <Sequence DisplayName="Main Logic" sap2010:WorkflowViewState.IdRef="Sequence_Main">
      <!-- Main workflow activities -->
    </Sequence>
  </TryCatch.Try>
  <TryCatch.Catches>
    <Catch x:TypeArguments="s:Exception">
      <ActivityAction x:TypeArguments="s:Exception">
        <ActivityAction.Argument>
          <DelegateInArgument x:TypeArguments="s:Exception" Name="exception" />
        </ActivityAction.Argument>
        <Sequence DisplayName="Handle Exception" sap2010:WorkflowViewState.IdRef="Sequence_HandleException">
          <Assign DisplayName="Set Failed Status">
            <Assign.Value>
              <InArgument x:TypeArguments="x:String">["FAILED"]</InArgument>
            </Assign.Value>
          </Assign>
          <ias:Append_Line ContinueOnError="True" DisplayName="Log Exception"
            Line="[&quot;EXCEPTION: &quot;+exception.Message+System.Environment.NewLine+&quot;StackTrace: &quot;+exception.StackTrace]"
            Source="[logFile]" />
        </Sequence>
      </ActivityAction>
    </Catch>
  </TryCatch.Catches>
</TryCatch>
```

**Required namespace** (add to Activity element):
```xml
xmlns:s="clr-namespace:System;assembly=mscorlib"
```

#### Pattern 2: ContinueOnError with If/Else (For Individual Operations)

Use `ContinueOnError="True"` with If/Else for operations that may fail but shouldn't crash the workflow:

```xml
<iao:ExtractDataActivity ContinueOnError="True" ResponseObject="[ocrResponse]" ... />
<If Condition="[ocrResponse Is Nothing]">
  <If.Then>
    <!-- Handle failure - set status, log error -->
  </If.Then>
  <If.Else>
    <!-- Handle success - continue processing -->
  </If.Else>
</If>
```

#### Pattern 3: API Response Code Validation

For API calls, always validate HTTP response codes:

```xml
<iai:IONAPIRequestWizard ContinueOnError="True" ResponseCode="[apiResponseCode]" Response="[apiResponse]" ... />
<If Condition="[apiResponseCode &lt; 200 OrElse apiResponseCode &gt;= 300]">
  <If.Then>
    <!-- Handle API error - HTTP status outside 200-299 range -->
    <Assign DisplayName="Set Failed Status">
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">["FAILED"]</InArgument>
      </Assign.Value>
    </Assign>
    <Assign DisplayName="Capture Error">
      <Assign.Value>
        <InArgument x:TypeArguments="x:String">["API failed with code "+apiResponseCode.ToString()+": "+If(apiResponse IsNot Nothing, apiResponse.readastext, "No response")]</InArgument>
      </Assign.Value>
    </Assign>
  </If.Then>
  <If.Else>
    <!-- Continue with success path -->
  </If.Else>
</If>
```

### Verbose Logging Best Practices

#### Log Full Payloads (Not Just Length)

**BAD** - Only logs length, useless for debugging:
```xml
<ias:Append_Line Line="[&quot;Payload length: &quot;+payload.Length.ToString()]" ... />
```

**GOOD** - Logs full content for debugging:
```xml
<ias:Append_Line Line="[System.Environment.NewLine+&quot;  Request Payload:&quot;+System.Environment.NewLine+payload]" ... />
```

#### Log API Requests BEFORE the Call

Always log the request payload before making API calls, so you can see what was sent even if the call fails:

```xml
<ias:Append_Line DisplayName="Log Request Payload" Line="[System.Environment.NewLine+&quot;  API Request:&quot;+System.Environment.NewLine+requestPayload]" ... />
<iai:IONAPIRequestWizard ... />
<ias:Append_Line DisplayName="Log Response" Line="[System.Environment.NewLine+&quot;  API Response Code: &quot;+responseCode.ToString()+System.Environment.NewLine+&quot;  Response: &quot;+If(response IsNot Nothing, response.readastext, &quot;null&quot;)]" ... />
```

#### Include Error Details in Final Log

When logging final results, include error messages for failures:

```xml
<ias:Append_Line Line="[&quot;Result: &quot;+status+If(status=&quot;FAILURE&quot; AndAlso errorMessage.Length &gt; 0, System.Environment.NewLine+&quot;  Error: &quot;+errorMessage, &quot;&quot;)]" ... />
```

#### Safe Null Handling in Logs

Always handle potential null values in log expressions:

```xml
<!-- WRONG - Crashes if apiResponse is null -->
<ias:Append_Line Line="[apiResponse.readastext]" ... />

<!-- CORRECT - Safe null handling -->
<ias:Append_Line Line="[If(apiResponse IsNot Nothing, apiResponse.readastext, &quot;null&quot;)]" ... />
```

### Sub-Workflow Error Message Propagation

When calling sub-workflows, capture error details via output arguments:

**Sub-workflow (e.g., SendToGenAIAgent.xaml):**
```xml
<x:Members>
  <x:Property Name="agentStatus" Type="OutArgument(x:String)" />
  <x:Property Name="agentErrorMessage" Type="OutArgument(x:String)" />
</x:Members>
```

**Calling workflow (MainPage.xaml):**
```xml
<iaw:InvokeWorkflow OutputArguments="[outputDict]" WorkflowFile="[subWorkflowPath]" ... />
<Assign DisplayName="Get Status">
  <Assign.Value>
    <InArgument x:TypeArguments="x:String">[If(outputDict IsNot Nothing AndAlso outputDict.ContainsKey("agentStatus"), CType(outputDict("agentStatus"), String), "FAILED")]</InArgument>
  </Assign.Value>
</Assign>
<Assign DisplayName="Get Error Message">
  <Assign.Value>
    <InArgument x:TypeArguments="x:String">[If(outputDict IsNot Nothing AndAlso outputDict.ContainsKey("agentErrorMessage"), CType(outputDict("agentErrorMessage"), String), "")]</InArgument>
  </Assign.Value>
</Assign>
```

### InvokeWorkflow OutputArguments (CRITICAL)

**WRONG - Nested OutputArguments** (causes "Activity could not be loaded" error):
```xml
<iaw:InvokeWorkflow WorkflowFile="[...]">
  <iaw:InvokeWorkflow.OutputArguments>
    <scg:Dictionary x:TypeArguments="x:String, Argument">
      <OutArgument x:TypeArguments="x:String" x:Key="status">[status]</OutArgument>
    </scg:Dictionary>
  </iaw:InvokeWorkflow.OutputArguments>
</iaw:InvokeWorkflow>
```

**CORRECT - Use Dictionary variable**:
```xml
<!-- Declare dictionary variable -->
<Variable x:TypeArguments="scg:IDictionary(x:String, x:Object)" Name="outputDict" />

<!-- Pass to InvokeWorkflow -->
<iaw:InvokeWorkflow OutputArguments="[outputDict]" WorkflowFile="[...]" />

<!-- Extract values after call -->
<Assign>
  <Assign.Value>
    <InArgument x:TypeArguments="x:String">[If(outputDict IsNot Nothing AndAlso outputDict.ContainsKey("status"), CType(outputDict("status"), String), "")]</InArgument>
  </Assign.Value>
</Assign>
```

Sub-workflows define outputs via x:Members:
```xml
<x:Property Name="status" Type="OutArgument(x:String)" />
```

### Sub-Workflow Invocation Path

RPA Studio caches workflow files in `AppData\Local\InforRPA\{ProjectName}\`. Use this pattern:

```xml
<Variable x:TypeArguments="x:String"
  Default="[Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)+&quot;\AppData\Local\InforRPA\{ProjectName}&quot;]"
  Name="projectPath" />

<iaw:InvokeWorkflow
  WorkflowFile="[projectPath+&quot;\SubWorkflow.xaml&quot;]"
  ContinueOnError="True" ... />
```

### OCR Activities

**Two OCR options available:**

#### 1. DocumentOC (Simple - Recommended)

Uses `Infor.RPA.OCR` namespace (`iro:`). Simpler and works without IDP flow configuration:

```xml
<iro:DocumentOC
  Pages="{x:Null}"
  ActivityID="e13e6163-56bd-4036-8cd2-0ea90be6a072"
  ContinueOnError="True"
  DisplayName="Get OCR Text"
  ExecuteFile="True"
  FilePath="[documentPath]"
  ErrorCode="[ocrErrorCode]"
  ResponseObject="[ocrResponse]" />
```

**Key Properties:**
- `FilePath` - Path to document (not `DocumentPath`)
- `Pages` - Optional page selection (use `{x:Null}` for all pages)
- `ResponseObject` - JToken output with extracted text

#### 2. ExtractDataActivity (Requires IDP Flow Setup)

Uses `Infor.Activities.OCR` namespace (`iao:`). Requires Infor Document Processor flow to be configured:

```xml
<iao:ExtractDataActivity
  ActivityID="f1deb545-9a42-4bea-a5bb-98a29721fcb6"
  OcrType="2"
  ContinueOnError="True"
  DocumentPath="[filePath]"
  ResponseObject="[ocrResponse]" />
```

**Note:** ActivityID references a specific IDP flow. Use existing ActivityIDs from working projects.

## Getting Help

### Understanding Existing Workflows
1. Open Main.xaml in RPA Studio
2. Review Variables/Arguments section for configuration
3. Follow workflow sequence visually
4. Check sub-workflow files for detailed operations
5. Look at project.json for dependencies

### Troubleshooting Workflows
1. Check Data Lake logs for execution history
2. Review error notification emails
3. Enable verbose logging via configuration flags
4. Test in development tenant first
5. Validate configuration parameters for target tenant

### Key Files for Context
- `CSIInvoiceProcessingGenAIV2/Main.xaml` - Most comprehensive example
- Any project's `project.json` - Understanding dependencies
- Sub-workflow XAMLs - Reusable component patterns

## Test Invoice Generation

The `DemoInvoiceLoader` project includes Python scripts to generate test PDF invoices for RPA workflow testing.

### Scripts Location
```
DemoInvoiceLoader/
├── generate_test_invoice.py      # Acme Supply vendor
├── generate_test_invoice_v2.py   # Global Parts Distribution vendor
└── generate_test_invoice_v3.py   # Precision Tools & Equipment vendor
```

### How to Generate Test Invoices
```bash
# Install fpdf2 library (one-time)
pip install fpdf2

# Generate a test invoice (outputs to C:\RPAFiles\OCR_TEST\Input)
python DemoInvoiceLoader/generate_test_invoice_v3.py
```

### Invoice Format for OCR
Invoices must include these labeled fields for successful OCR extraction:
- `Vendor Name:` - Required
- `Vendor Address:` - Optional (parsed for city, state, zip)
- `Vendor Phone Number:` - Optional
- `Vendor Email Address:` - Optional
- `Purchase Order Number:` - Required
- `Order Date:` - Optional (defaults to current date)

Line items table must have columns:
- `Line Number` | `Item Code` | `Description` | `Quantity Shipped` | `UOM`

### Output Location
Generated PDFs are saved to: `C:\RPAFiles\OCR_TEST\Input\`

This is the default input folder for the DemoInvoiceLoader RPA workflow.

---

**Note**: This repository requires Infor RPA Studio to open and edit workflows. XAML files can be viewed in text editors but workflow logic is best understood visually in the Studio IDE.

