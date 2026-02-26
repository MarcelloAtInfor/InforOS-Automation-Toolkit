# Infor SyteLine IDO Collections Reference

This document provides a comprehensive list of all available IDO (Intelligent Data Objects) collections in Infor SyteLine.

## Overview

Total IDO Collections: **915**

## IDO Collections by Project

### Adapters (6 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLCurrencies | Currency Integration Adapter (XML document interface) | Currencies |
| SLOrderStatuses | Order Status Integration Adapter (XML document interface) | Order Statuses |
| SLPartySyncs | Party Synchronization Integration Adapter (XML document interface) | Party Synchronizations |
| SLPriceQuotes | Price Quote Integration Adapter (XML document interface) | Price Quotes |
| SLProductCatalogs | Product Catalog Integration Adapter (XML document interface) | Product Catalogs |
| SLPurchaseOrders | Purchase Order / Quote Integration Adapter (XML document interface) | Purchase Orders |

### Admin (30 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLApplicationDebugLogs | Application debug message logs | oSLApplicationDebugLogs |
| SLApplicationModules | Date Management - List of Modules | Application Modules |
| SLAppWorkflows | IDO for application system event handlers. | Application Workflows |
| SLCalculators | Dummy IDO for SyteLineCalculator | Calculators |
| SLDbMaintParms | Database Maintenance Parameters | odb_maint_parms |
| SLDocProfileEmailTemplates | Document Profile Email Templates | oSLDocProfileEmailTemplates |
| SLDocumentObjectAndRefExtViews | Document Object Reference Extended View | Document Object And Reference Extended Views |
| SLDocumentObjectGroupViews | Document Object Group View | Document Object Group Views |
| SLDocumentObjects_Exts | Document Object Extended | Document Objects Extends |
| SLDocumentTypeGroups | Document Type Groups | Document Type Groups |
| SLElectronicSignatures | Electronic Signatures | Electronic Signatures |
| SLEsigAuthorizations | SLEsigAuthorization | Signature Types |
| SLEventMessages | IDO for the Portal Administrator Home | Event Messages |
| SLEventStates | IDO used for Portal Administrator Home | Event States |
| SLExtPRInterfaceErrors | External Payroll Interface | External Payroll Interface Errors |
| SLExtPRInterfaces | External Payroll Interface | External Payroll Interfaces |
| SLFormActionThresholds | Form Action Thresholds | oFormActionThresholds |
| SLFormAdoption | Form Adoption | Form Adoption |
| SLJourHdrs | Jounal Header Information | Jounal Headers |
| SLLockableFunctions | Unlock Locked Functions | Lockable Functions |
| SLMsgBwsrs | Message Query | Message Browsers |
| SLObjectMainMessages | Message Query | Object Main Messages |
| SLOptionalModules | ooptionalmodules | ooptionalmodules |
| SLPortalsDocumentObjectGroupViews | Document Object Group View | Document Object Group Views |
| SLRefreshData | IDO for CSI Suite Refresh |  |
| SLReleaseManagement | Release Management for upgrade | oReleaseManagement |
| SLSiteMgmtTableData | Site Management Table Data | Site Migration Table Data |
| SLTenantDataCleanup | CSI Tenant Data Cleanup API |  |
| SLTmpDbMaintCompressions | used to display generated SQL statements by ProcessCompression method | oSLTmpDbMaintCompression |
| SLUserFormPreferences | User Form Preferences | User Form Preferences |

### APS (50 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAltplans | Used by the Planning Mode and Planning Parameters forms.  Bound to ALTPLAN | Alternate Plans |
| SLAPSDataVisualization | IDO for APS Data Visualization Hub | APS Data Visualization |
| SLApsParmAlls | Planning Mode Multi-Site | oApsParmAlls |
| SLApsParms | Planning Mode | APS Parameters |
| SLApsplandetails | Replicate planning detail to other sites when running the Planning activity in single-site mode | APS Plan Details |
| SLApsRes | Used in validator - ApsResourceInColl | APS Resource |
| SLApsSeqs | MRP-APS Order Priority | APS Sequences |
| SLApsSites | Used by the Planning Parameters form. Bound to aps_site | APS Sites |
| SLContention | Contention | oContention |
| SLContentionDetails | Contention Details | oContentionDetails |
| SLCtps | Contains methods used by the CTP process | Capacities |
| SLDemandSummaries | Demand Summary MRP-APS | Demand Summaries |
| SLDown000s | Used by the Resource Gantt Chart form. Bound to DOWN000, an APS Scheduler output table used to record periods of resource unavailability | Downs |
| SLDownplan000s | Bound to DOWNPLAN000, an APS Scheduler output table used to record periods of resource unavailability | Down Plans |
| SLGantt | Contains method used by Gantt charts |  |
| SLGNTHLCATs | Used by the Resource Gantt Chart. Tied to GNTHLCAT table (catalog of user-defined highlights - names only) | oGNTHLCATs |
| SLGNTHLCRITs | Used by the Resource Gantt Chart. Tied to GNTHLCRIT table (contains one or more criteria that define each highlight) | Gantt Chart High Light Criterias |
| SLGNTPREFSs | Used by the Resource Gantt Chart. Tied to GNTPREFS table (Gantt User Preferences) | Gantt User Preferences |
| SLGNTSELCATs | Used by the Resource Gantt Chart. Tied to GNTSELCAT table (catalog of user-defined resource selections -  group of resources selected for viewing in Gantt chart) | Gantt Chart Selection Catlogs |
| SLGNTSELMBRs | Used by the Resource Gantt Chart. Tied to GNTSELMBR (contains the names of the resources for each resource selection) | Gantt Chart Selection Members |
| SLInventoryLevels | Inventory Level form | Inventory Levels |
| SLInventorySummaries | Inventory Summary form | Inventory Summaries |
| SLInvplan000s | Bound to INVPLAN000, an APS Scheduler output table used to record supply and demand that affects material inventory | Inventory Plans |
| SLJobplan000s | Bound to JOBPLAN000, an APS Scheduler output table used to record information about each operation in the plan | Job Plans |
| SLLateJobs | Late Jobs | Late Jobs |
| SLLOOKUP000s | Setup Matrix | Lookups |
| SLLookuphdrs | Used by the Setup Matrix form. Bound to LOOKUP000, an APS Scheduler table used for looking up a value based on two parameters | Lookup Headers |
| SLMATLALTnnns | Planner ALTernate MATL ID cross reference | Material Alternates |
| SLMATLATTRnnns | Planner ATTribute ID corss reference | Material Attributes |
| SLMATLnnns | Planner Items - MATERIAL ID | Materials |
| SLMATLPBOMSnnns | Planner BOM ID Cross reference | Material Planner BOM Sources |
| SLMatlplan000s | Bound to MATLPLAN000, an APS Scheduler output table that summarizes schedule event records | Material Planners |
| SLMATLPPSnnns | Planner PROCedure PLAN ID cross reference | Material Planner Procedure Sources |
| SLOrdplan000s | Bound to ORDPLAN000, an APS Scheduler output table used to record projected dates for planned orders | Order Plans |
| SLPBOMMATLSnnns | Planner BOM Materials | Planner BOM Materials |
| SLPBOMnnns | Planner BOM | Planner BOMs |
| SLPROCPLNnnns | Planner PROCedure PLaN | Procedure PLans |
| SLPushPassSettings | APS Push Pass Setting | Push Pass Settings |
| SLResourceGroupUtilizations | Resource Group Utilization | Resource Group Utilizations |
| SLResourcePlans | Resource Plan | Resource Plans |
| SLResourceUtilizations | Resource Utilization MRP-APS | Resource Utilizations |
| SLRGBottleneckDetails | Resource Group Bottleneck Details | Resource Group Bottleneck Details |
| SLRGBottlenecks | Resource Group Bottlenecks | Resource Group Bottlenecks |
| SLSchedDemandDetails | Demand Detail - Scheduler | Schedule Demand Details |
| SLSchedDemandSummaries | Demand Summary - Scheduler | Schedule Demand Summaries |
| SLShortageDetails | Shortage Details -  Report | Shortage Details |
| SLShortages | Shortages - Report | Shortages |
| SLSupplyUsageDemands | Supply Usage MRP-APS - demand subcollection | Supply Usage Demands |
| SLSupplyUsages | Supply Usage MRP-APS | Supply Usages |
| SLWait000s | 'Bound to WAIT000, an APS Scheduler output table used to record waiting time for the Planner" | Waits |

### BusInterface (4 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLTmpAckPoBlns | Temp table used for importing PO Acknowledgements | Temporary Acknowledgement Purchase Order Blankets |
| SLTmpAckPoitems | Temp table for importing PO Acknowledgements | Temporary Acknowledgement Purchase Orders Items |
| SLTmpAckPos | Temp table used for importing PO Acknowledgements | Temporary Acknowledgement Purchase Orders |
| SLTmpExportPoRcpts | Handles the temp table for PO receipt exports | Temporary Export Purchase Order Receipts |

### Codes (80 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAccountAuthorizations | Account Authorizations | Account Authorizations |
| SLCostCodes | Project Cost Codes | Cost Codes |
| SLCountries | Countries | Countries |
| SLCurrates | Currency Rates | Currency Rates |
| SLCurrencyCodeAlls | Multi Site Currency Codes | Currency Code Alls |
| SLCurrencyCodes | Currency Codes | Currency Codes |
| SLCurrParms | Currency Parameters | Currency Parameters |
| SLCurrUks | Excise Currency Rates | Currency Uks |
| SLCusttypes | Customer Types | Customer Types |
| SLDelTermAlls | Delivery Terms All | Delivery Term Alls |
| SLDelTerms | Delivery Terms | Delivery Terms |
| SLDimAttributes | Dimension Attributes | Dimension Attributes |
| SLDimensionObjects | Dimension Objects | oSLDimensionObjects |
| SLDimensions | Dimensions | oSLDimensions |
| SLDimFunctions | Dimension Functions | oSLDimFunctions |
| SLDimObjectAttributeInlineList | Dimension Object Attributes Inline List | oSLDimObjectAttributeInlineList |
| SLDimObjectAttributes | Dimension Object Attributes | oSLDimObjectAttributes |
| SLDimObjectTableJoins | Dimension Object Table Joins | Dim Object Table Joins |
| SLDimSubscribers | Dimension Subscribers | oSLDimSubscribers |
| SLDistAcctAlls | Distribution Accounts | Distribution Account Alls |
| SLDistAccts | Distribution Accounts | Distribution Accounts |
| SLEsigTypes | SLEsigType | Electronic Signature Types |
| SLEvalcodes | Evaluation Codes | Evaluation Codes |
| SLFabonuses | Bonus Depreciation Codes | Fixed Asset Bonus Depreciation Codes |
| SLFaclasses | Fixed Asset Class Codes | Fixed Asset Class Codes |
| SLHorizons | Planning Horizon Calendar | Horizons |
| SLIncoDelTerms | INCOTERM 2000 codes | International Commercial Dellivery Terms |
| SLISOBankTranDomainFamilies | ISO Bank Transaction Domain Family Codes | oISOBankTranDomainFamilies |
| SLISOBankTranDomains | ISO Bank Transaction Domain Codes | oISOBankTranDonains |
| SLISOBankTranDomainSubFamilies | ISO Bank Transaction Domain Sub Family | oISOBankTranDomainSubFamilies |
| SLISOCountries | ISO Countires | ISO Countries |
| SLISOCurrencyCodes | ISO Currency Codes | ISO Currency Codes |
| SLISOUMs | ISO Unit of Measure Codes | ISO Unit of Measures |
| SLItemContentExchanges | Item Content Exchanges | oitem_content_exchanges |
| SLItemContentPrices | Item Content Prices | oSLItemContentPrices |
| SLItemContents | Item Contents | oitem_contents |
| SLMachineDowntimeCodes | Machine Downtime Codes | Machine Downtime Codes |
| SLObjectNotes | Notes - primary data source | Object Notes |
| SLParms | General Parameters | System Parameters |
| SLProdcodeAlls | Product Codes - All | Prodcode Alls |
| SLProdcodes | Product Codes | Product Codes |
| SLProjtypes | Project Types | Project Types |
| SLReasons | Used for various Reason Codes | Salary Change Reasons |
| SLRetentions | Project Retention Codes | Retentions |
| SLRetScheds | Project Retention Codes - grid | Retention Schedules |
| SLShifts | Shift Codes | Shifts |
| SLShipcodeAlls | Ship Via Codes All | Ship Code Alls |
| SLShipcodes | Ship Via Codes | Ship Codes |
| SLShipTos | Drop Ship To | Ship Tos |
| SLSiteGroupsSelection | SL Site Groups Selection | oSLSiteGroupsSelection |
| SLSitesSelection | SL Sites Selection | oSLSitesSelection |
| SLStates | Prov/States | States |
| SLTaxcodeAlls | Tax Codes - All | Tax Code Alls |
| SLTaxcodes | Tax Codes | Tax Codes |
| SLTaxItemJurs | Tax Codes for Items by Jurisdiction | Tax Item  Jurisdictions |
| SLTaxJurs | Tax Jurisdiction | Tax Jurisdiction |
| SLTaxparms | Tax Parameters | Tax Parameters |
| SLTaxSystems | Tax Systems | Tax Systems |
| SLTerms | Billing Terms | Terms |
| SLTermsSeqs | Billing Terms - track the sequence of a multiple due date record | Terms Sequences |
| SLTransNature2s | Secondary Nature of Transaction Codes | Transaction Secondary Natures |
| SLTransNatureAlls | Nature of Transaction Codes All | Transaction Nature Alls |
| SLTransNatures | Nature of Transaction Codes | Transaction Natures |
| SLUMAlls | Unit of Measure Conversions All | Unit of Measure Alls |
| SLUMConvs | Unit of Measure Conversions | Unit of Measure Conversions |
| SLUMs | Unit of Measure Codes | UMs |
| SLUserLocals | Users - Additional Info tab | User Locals |
| SLUserNames | Extends UserNames and includes user_local |  |
| SLVatProceduralMarkingAlls | Vat Procedural Marking Alls | VAT Procedural Marking All |
| SLVatProceduralMarkingDefaults | Vat Procedural Marking Default | VAT Procedural Marking Default |
| SLVatProceduralMarkings | Vat Procedural Markings | VAT Procedural Markings |
| SLVchProceduralMarkingAlls | Voucher Procedural Markings - All | Voucher Procedural Markings |
| SLVchProceduralMarkings | Voucher Procedural Markings | Voucher Procedural Markings |
| SLWcompAuthorities | Workers' Compensation Authority | Workers’ Compensation Authority |
| SLWcompDCOs | Workers' Compensation Data Collection Organization | Workers’ Compensation Data Collection Organization |
| SLWcompInitialTreatments | Workers’ Compensation Initial Treatment Codes | Workers’ Compensation Initial Treatment Codes |
| SLWcompInjuryCodes | Workers’ Compensation Injury Codes | Workers’ Compensation Injury Codes |
| SLWcompInjuryGroups | Workers’ Compensation Injury Groups | Workers’ Compensation Injury Groups |
| SLWcompInsurers | Workers’ Compensation Insurer | Workers’ Compensation Insurer |
| SLWcompPolicies | Workers’ Compensation Policy | Workers’ Compensation Policy |

### Config (9 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLCfgAttrAlls | Configuration Attributes All Table | Configuration Attribute Alls |
| SLCfgAttrs | Configuration Attributes | Configuration Attributes |
| SLCfgCompAlls | Configuration Components All Table | Configuration Components Alls |
| SLCfgComps | Configuration Components | Configuration Components |
| SLCfgCustomGroupFields | List of fields from Item and Work Center tables that can be mapped to Custom Groups and Custom Parts in SC Config Powerpack Manager | Configuration Custom Group Fields |
| SLCfgMains | Configuration Header | Configuration Mains |
| SLCfgRefs | Configuration References | Configuration References |
| SLCfgSchemaAttributeFields | List of fields that can be mapped to Schema Attributes in SC Config Powerpack Manager | Configuration Schema Attribute Fields |
| SLForms | Forms used to select Configuration Parts and Attribute Values |  |

### Customer (172 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAcks | Retransmit EDI invoices, ASNs, Planning Schedules, Acknowledgements | Acknowledgements |
| SLARCustomerBankAccounts | AR Customer bank account |  |
| SLARDirectDebit | A/R Direct Debit | oARDirectDebits |
| SLArDraftts | Possibly used for A/R Draft Remittance, or may be obsoleted by SLCustdrfts | AR Drafts |
| SLArEftImportArpmtds | AR Payment Distributions | AR EFT Import Distributions |
| SLArEftImportArpmts | AR Payments | AR EFT Import Payments |
| SLArfins | Finance Charge Posting | AR Finances |
| SLArinvAlls | nvoices, Debit and Credit Memos All | AR invoice Alls |
| SLArinvds | Invoices, Debit and Credit Memos G/L Distribution | AR Invoice Distributions |
| SLArinvItems | For Manual Invoice Items | Invoice Items |
| SLArinvs | Invoices, Debit and Credit Memos | AR Invoices |
| SLArparms | Accounts Receivable Parameters | Account Receivable Parameters |
| SLARPaymentImportConversions | A/R payment import conversions | A/R payment import conversions |
| SLARPaymentImportMapFields | A/R Payment Import Field Mappings |  |
| SLARPaymentImports | AR Payment Imports | oSLARPaymentImports |
| SLArpmtds | A/R Payment Distributions | AR Payment Distributions |
| SLArpmts | A/R Payments | AR Payments |
| SLArTermsDueAlls | Multiple Due Date Invoice | AR Terms Due Alls |
| SLARTermsDues | Multiple Due Date Invoice | A/R Terms Dues |
| SLArtranAlls | A/R Posted Transactions All | AR Transaction Alls |
| SLArtrans | A/R Posted Transactions | AR Transactions |
| SLArtranSiteAlls | A/R Posted Transactions All, it includes data from all the sites | AR Transaction Site Alls |
| SLCampaignCommunications | Marketing Campaign Communications | Campaign Communications |
| SLCampaignContacts | Marketing Campaign Contacts | Campaign Contacts |
| SLCampaignItems | Marketing Campaign Items | Campaign Items |
| SLCampaigns | Marketing Campaigns | Campaigns |
| SLCampaignStatuses | Marketing Campaign Statuses | Campaign Statuses |
| SLCampaignTypes | Marketing Campaign Types | Campaign Types |
| SLCarrierShip | Carrier Shipments Table for UPS/FedEx Integration | Carrier Ship |
| SLChargebacks | Chargeback | Chargeback |
| SLChargebackTypes | Chargeback Type | Chargeback Type |
| SLCitemhs | History Customer Order Lines and History Customer Order Blanket Releases | Customer Order Item Historys |
| SLCoAlls | Customer Orders All - site_ref and co_num as key | Customer Order Alls |
| SLCoBlns | Customer Order Blanket Lines | Customer Order  Blankets |
| SLCohAlls | History Customer Orders All | Customer Order History Alls |
| SLCohBls | History Customer Order Blanket Lines | Customer Order Blanket Historys |
| SLCohs | History Customer Orders All | Customer Order History Alls |
| SLCoitemAlls | Customer Order Lines and a lot of related forms | Customer Order Line Alls |
| SLCoitemLogs | Customer Order Lines Change Log | Customer Order Lines Logs |
| SLCoitems | Customer Order Lines and a lot of related forms | Order Lines |
| SLCoitemShps | Order Shipping and related forms | Customer Order Ships |
| SLCommdues | Commissions Due | Commission Dues |
| SLCommtabs | Commission Table Maintenance | Commission Tables |
| SLConInvHdrs | Consolidated Invoice Generation and Consolidated Invoices Workbench | Consolidated Invoice Headers |
| SLConInvItems | Consolidated Invoice - Summarized Line Detail Info (used in conjunction with SLConInvLines) - for each con_inv_line table record there will be one or more con_inv_item table records. | Consolidated Invoice Items |
| SLConInvLines | Consolidated Invoice - Summarized Line Info | Consolidated Invoice Lines |
| SLContactAlls | Conctact Details for all sites | oConctacts |
| SLContactgroupContacts | Sub Collection for SLContactgroups | Contact Group Contacts |
| SLContactgroups | Primary IDO for Sales Contact Group | Contact Groups |
| SLContacts | Contact Details | Contacts |
| SLCoPackingSlips | Pre-Ship Packing Selection | Customer Order Packing Slips |
| SLCoparmAlls | Order Entry Parameters | Customer Parameter Alls |
| SLCoparms | Order Entry Parameters | Customer Parameter |
| SLCos | Customer Orders and a lot of related forms | Customer Orders |
| SLCoShipApprovalLogs | Co Ship Approval Logs | oCoShipApprovalLogs |
| SLCoShips | Order Shipments and History Order Shipments | Customer Order Ships |
| SLCoSlsComms | Sales Commission Distribution and related forms | Distributions |
| SLCustAddrs | Access custaddr table info in some A/R and Customer forms | Customer Addresses |
| SLCustLcrs | Customer Letters of Credit | Customer Letters of Credits |
| SLCustomerAlls | Customers All | Customer Alls |
| SLCustomerContacts | Customer Contacts |  |
| SLCustomerCurrency | Customer Currency Code | Customer Currencies |
| SLCustomerPortalCoitems | IDO used only by the Customer Portal | Customer Portal Coitems |
| SLCustomers | Customers | Customers |
| SLCustomerStatuses | Customer Statuses | Customer Statuses |
| SLCustomerSurchargeRules | Customer Surcharge Rules | ocust_surcharge_rules |
| SLCustomerUsernames | Customer Usernames | Customer Usernames |
| SLCustTps | EDI Customer Profiles | EDI Customer Profiles |
| SLDiscounts | Discounts by Customer Type and Product Code | Discounts |
| SLDispcodes | Disposition Codes | Disposition Codes |
| SLDocProfileCustomers | Customer Doc Profiles | Doc Profile Customers |
| SLDoHdrs | Delivery Order Header Information | Delivery Orders |
| SLDoLines | Delivery Order Line Information | Delivery Order Lines |
| SLDoSeqs | Delivery Order Line Sequences | Sequences |
| SLDropshiptos | Drop Ship To Query | Drop Ship Tos |
| SLEdiBols | EDI Advance Ship Notices | EDI Bill of Ladings |
| SLEdiCoblns | EDI Customer Order Blanket Lines | EDI Customer Order Blanket Lines |
| SLEdiCoitems | EDI Customer Order Blanket Lines and Releases | EDI  Customer Order lines |
| SLEdiCos | EDI Customer Orders | EDI Customer Order |
| SLEdiInvHdrs | EDI Invoice Register Header | EDI Invoice Headers |
| SLEdiParms | Demand EDI Parameters | EDI Parameters |
| SLEndTypeAlls | End Type All | End Type Alls |
| SLEndtypes | End User Types | End Types |
| SLFavoriteCustomers | My Favorite Customer | ofavorite_customers |
| SLFeatqties | Customer Orders - Feature Groups info | Feature Quantities |
| SLInteractionTopics | Interaction Topics | Interaction Topics |
| SLInvBatchDetails | Invoice Batch Details | Invoice Batch Details |
| SLInvBatchs | Invoice Batchs | Invoice Batches |
| SLInvCategories | It's a collection of Invoice categories from inv_category table( Used in Invoice Categories, Void Unused Invoices, Invoice / Credit Memo / Debit Memo Sequences Forms) | Invoice Categories |
| SLInvcLangs | Multi-Lingual Order Invoice | Invoice Languages |
| SLInvHdrAlls | Order Invoicing Credit Memo and RMA Cred | Invoice Headers |
| SLInvHdrs | Order Invoicing Credit Memo and RMA Credit Memo | Invoice Headers |
| SLInvItemAlls | Invoice Listing | Invoice Item Alls |
| SLInvoiceBuilders | Used for Invoice Builder Form | Invoice Builders |
| SLInvSequences | Its the collection that is used in the Invoices /Credit/ Debit Memo Sequences form. It uses the inv_sequences table along with the inv_category table to take the description of the category. | Invoice Sequences |
| SLInvVoids | It will be used for Voiding Invoice Numbers,Base Table for this IDO is inv_void. ( Used in Voided Invoices , Void Unused Invoices Forms) | Invoice Voids |
| SLItemContentRefs | Item Content References | oitem_content_refs |
| SLItemCustPriceAlls | Customer Item Cross Reference Prices | Item Customer Prices |
| SLItemCustPrices | Customer Item Cross Reference Prices | Item Customer Prices |
| SLItemcusts | Customer Item Cross References | Cross References |
| SLLeadAlls | Leads | Lead Alls |
| SLLeads | Leads | Leads |
| SLLeadStatuses | Lead Statuses | Lead Statuses |
| SLOPMMethods | OPMMethods |  |
| SLOpportunities | Opportunities | Opportunities |
| SLOpportunityAlls | Opportunities | Opportunity Alls |
| SLOpportunityMembers | Opportunity Members | Team Members |
| SLOpportunitySources | Opportunity Sources | Opportunity Sources |
| SLOpportunityStages | Opportunity Stages | Opportunity Stages |
| SLOpportunityStatuses | Opportunity Status | Opportunity Statuses |
| SLOpportunityTaskAlls | Opportunity Tasks | Opportunity Task Alls |
| SLOpportunityTasks | Opportunity Tasks | Tasks |
| SLOpportunityTaskTypes | Opportunity Task Types | Opportunity Task Types |
| SLPackWorkbenchs | Pack Workbench | Pack Workbenchs |
| SLPckHdrs | Packing Slip info (used in utilities) | Packing Headers |
| SLPckitems | Used for Packing Slip on Invoice | Packing Items |
| SLPickLists | Pick Lists | Pick Lists |
| SLPickWorkbenchs | Pick Workbench | Pick Workbenchs |
| SLPkgLabelTemplates | Package Label Templates | Package Label Templates |
| SLPortalCompanyProfile | Created for Customer Portal My Compny Profile web page | Portal Company Profile |
| SLPortalCompanyShipTos | Created for Customer Portal My Compny Profile web page | Portal Company Ship Tos |
| SLPostedARTermsDues | ARPostedInvoiceDueDates - update the date on invoices with multiple due dates | AR Posted Invoice Due Dates |
| SLPostedInvs | Posted Invoices | Posted Invoices |
| SLPriAdjInvs | Used on the Price Adjustment Invoice forms | Price Adjustment Invoices |
| SLPriceformulas | Price Formulas | Price Formulas |
| SLPricematrixs | Price Matrix | Price Matrixs |
| SLPricePromotions | Promotion Codes for Promotional and Reba | oPricePromotions |
| SLProbcodes | Problem Codes | Problem Codes |
| SLProFormaInvHdrAlls | Pro Forma Invoice Header Alls | opro_forma_inv_hdr_alls |
| SLProFormaInvHdrs | Pro Forma Invoice Header | oProFormaInvoiceHeader |
| SLProFormaInvItems | Pro Forma Invoice Items | Pro Forma Invoice Items |
| SLProFormaStaxs | Pro Forma Invoice Sales Tax | sProFormaInvoiceSalesTax |
| SLProgbills | Progressive Billings - grid | Progressive Billings |
| SLProspectAlls | Prospect | Prospect Alls |
| SLProspectContacts | Prospect Contacts | Prospect Contacts |
| SLProspects | Prospect | Prospects |
| SLReports | Used to get current year or report labels in some reports | Reports |
| SLRmaitemAlls | RMA Line Items | Return Material Authorization Items |
| SLRmaitems | RMA Line Items | Return Material Authorization Items |
| SLRmaitmLogs | Delete RMA Item Log Entries | Return Material Authorization Item Logs |
| SLRmaparms | RMA Parameters | Return Material Authorization Parameters |
| SLRmarepls | RMA Line Items - Replacement Lines | Return Material Authorization Replacements |
| SLRmas | RMAs | Return Material Authorizations |
| SLSalesForecastOpportunities | Primary Collection of Sales Forecast Opportunity | Sales Forecast Opportunities |
| SLSalesForecasts | Primary Collection for Sales Forecast | Sales Forecasts |
| SLSalesPeriods | Primary Collection for Sales Period | Sales Periods |
| SLSalesTeamMembers | Sales Team Members | Sales Team Members |
| SLSalesTeams | Sales Teams | Sales Teams |
| SLShipCos | Shipping Processing Orders | Ship Customer Orders |
| SLShipItems | Shipping Processing Line Releases | Ship Items |
| SLShipLangs | Multi Lingual Ship Via | Ship Languages |
| SLShipmentLines | Shipment Master Lines | Shipment Lines |
| SLShipmentPackages | Shipment Master Packages | Shipment Packages |
| SLShipmentRefCharges | Shipment Reference Charges | Shipment Reference Charges |
| SLShipments | Shipment Master | Shipments |
| SLShipmentSeqs | Shipment Seqs - Package Contents | Shipment Sequences |
| SLShipmentSeqs_FT | Shipment Seqs - Package Contents | oshipment_seqs |
| SLShipmentSeqSerials | Shipment Seq Serials - Packaged Serial Numbers | Shipment Sequence Serials |
| SLShipmentSeqUnpacks | Shipment Unpack Inventory | Shipment Sequence Unpacks |
| SLShipProcs | Shipping Processing Batches | Ship Processes |
| SLSlsclass | Salesperson Classifications | Salesperson Classifications |
| SLSlsmans | Salespersons | Salesmans |
| SLSSDs | EC SSDs and Project Resource Shipping SSDs | Supplementary Statistical Declarations |
| SLTermLangs | Multi Lingual Terms | Term Languages |
| SLTerritories | Territories | Territories |
| SLTmpCoShips | Pre-Ship Packing Selection - Shipping tab | Temporary Customer Order Ships |
| SLTmpInvoiceBuilders | Used in Invoice Builder | Temporary Invoice Builders |
| SLTmpShipSeqs | Temperary Table for Shipment Seq Records | Temporary Ship Sequences |
| SLTmpShipSeqSerials | Temperary Table for Shipment Sequence Serials | Temporary Ship Sequence Serials |
| SLTTInvAdjs | Interface to temporary table tt_inv_adj | Temporary Table Invoice Adjustments |
| SLTTPmtpcks | Interface to temporary table tt_pmtpck | Temporary Table Prompt Packs |
| SLTTTaxDists | Interface to temporary table tt_tax_dist | Temporary Table Tax Distributions |

### DataCollection (25 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLDccos | Customer Order Shipping Error Processing | Data Collection Customer Orders |
| SLDccoSerials | Customer Order Shipping Error Processing - Serial Numbers tab | Data Collection Customer Order Serials |
| SLDcitems | Cycle Counting Error Processing | Data Collection Items |
| SLDcitemSerials | Cycle Counting Error Processing - Serial Numbers tab | Data Collection Item Serials |
| SLDcjits | Just-in-Time Production Error Processing | Data Collection Just in Times |
| SLDcjitSerials | Just-in-Time Production Error Processing - Serial Numbers tab | Data Collection Just in Time Serials |
| SLDcjms | Job Material Transactions Error Processing | Data Collection Job Materials |
| SLDcjmSerials | Job Material Transactions Error Processing - Serial Numbers tab | Data Collection Job Materials Serials |
| SLDcmoves | Quantity Move Error Processing | Data Collection Moves |
| SLDcmoveSerials | Quantity Move Error Processing - Serial Numbers tab | Data Collection Move Serials |
| SLDcparms | Data Collection parameters | Data Collection Parameters |
| SLDcphyinvs | Used for Physical Inventory Error Processing | Data Collection Physical Inventories |
| SLDcpos | Purchase Order Receiving Error Processing | Data Collection Purchase Orders |
| SLDcpoSerials | Purchase Order Receiving Error Processing - Serial Numbers tab | Data Collection Purchase Order Serials |
| SLDcpss | Production Schedule Complete Error Processing | Data Collection Production Schedules |
| SLDcpsSerials | Production Schedule Complete Error Processing - Serial Numbers tab | Data Collection Production Schedule Serials |
| SLDcsfcItems | Job Error Processing - item info | Data Collection Shop Floor Control Items |
| SLDcsfcs | Data Collection; Work Center Machine/Labor Time Error Processing | Data Collection Shop Floor Controls |
| SLDcsfcSerials | Job Error Processing - Serial Numbers tab | Data Collection Shop Floor Control Serials |
| SLDctas | Data collection time and attendance | Data Collection Time Attendances |
| SLDctrans | Transfer Order Receive Error Processing | Data Collection Transactions |
| SLDctranSerials | Transfer Order Receive Error Processing - Serial Numbers tab | Data Collection Transaction Serials |
| SLDcwcs | Work Center Material Error Processing | Data Collection Work Centers |
| SLDcwcSerials | Work Center Material Error Processing - Serial Numbers tab | Data Collection Work Center Serials |
| SLTimeatts | Time & Attendance Log | Time Attendances |

### DELOC (3 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLGDPdUMedia | Media Set for GDPdU Reports | oSLGDPdUMedia |
| SLGoBDUMedia | Media Set for GoBDU Reports | oSLGoBDUMedia |
| SLTmpGobdMediaDatas | Media Data Index for Gobd Reports | GoBD Media Data |

### Employee (88 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAbsences | Absence Reasons | Absences |
| SLAdpParms | ADP integration parameters | Adp Parameters |
| SLAppEds | Applicant Education | Applicant Educations |
| SLAppInts | Applicant Interviews | Applicant Interviews |
| SLApplicants | Applicants | Applicants |
| SLAppRefs | Applicant Reference | Applicant References |
| SLAppSources | Application Sources | Application Sources |
| SLAwards | Awards/Citations | Awards |
| SLCertifications | Certifications/Licenses | Certifications |
| SLCourses | Training Courses | Courses |
| SLDepDtlss | Magnetic Media Direct Deposit | Direct Deposits |
| SLDepts | Departments | Departments |
| SLDeptSupvs | Department Supervisors | Department Supervisors |
| SLDivMgrs | Divisions | Division Managers |
| SLEdMajors | Education Majors | Education Majors |
| SLEEOClss | EEO Class | Equal Employment Opportunity Classes |
| SLEmpAbsences | Attendance | Employee Absences |
| SLEmpawards | Employee Awards | Employee Awards |
| SLEmpCategories | Employee Categories | oSLEmpCategories |
| SLEmpCerts | Applicant or Employee Certification/License | Employee Certifications |
| SLEmpChilds | Children | Employee Childs |
| SLEmpConts | Emergency Contacts | Emergency Contacts |
| SLEmpEds | Employee Education | Employee Educations |
| SLEmpexams | Applicant or Employee Exams | Employee Exams |
| SLEmpHpos | Employee Position History | Employee History Position |
| SLEmpI9s | Employment Eligibility | Employment Eligibility |
| SLEmpInjuries | Employee Injuries | Employee Injuries |
| SLEmpInss | Employee Insurance | Employee Insurances |
| SLEmpinssDependents | Employee Insurance Dependents | oEmpinssDependents |
| SLEmployees | Employees | Employees |
| SLEmployeesInternal | Internal methods of employees IDO. Not part of any license or permission group. | oEmployeesInternal |
| SLEmpMemos | Employee Memos | Employee Memos |
| SLEmpPoss | Employee Positions | Employee Positions |
| SLEmpPrBanks | Employee - Direct deposit |  |
| SLEmpProps | Employee Properties | Employee Properties |
| SLEmpRas | Employee Reimbursement Plans | Employee Reimbursement Plans |
| SLEmpreviews | Employee Performance Reviews | Employee Reviews |
| SLEmpSalaries | Employee Salaries | Employee Salaries |
| SLEmpSelfServPreqitems | Created for the Employee Self Service Module |  |
| SLEmpSelfServPreqs | Created for the Employee Self SErvice Module |  |
| SLEmpSelfServPrtrxps | Used by Employee Self Service module |  |
| SLEmpSelfServPTOAccruedTakenBal | Created for Employee Self Service Module | oSLEmpSelfServPTOAccruedTakenBal |
| SLEmpSelfServTimeOffCalendar | Created for the Employee Self Service Module | oSLEmpSelfServTimeOffCalendar |
| SLEmpskills | Employee Skills | Employee Skills |
| SLEmpStats | Employee Status | Employee Statuses |
| SLEmpSteps | Applicant or Employee Processing | Employee Steps |
| SLEmpWrkExps | Employee Work Experience | Employee Work Experiences |
| SLEthnicIds | Ethnic Id | Ethnic Ids |
| SLExams |  | Exams |
| SLExperiences | Work Experience | Work Experiences |
| SLHrparms | Human Resources Parameters | Human Resource Parameters |
| SLHrSteps | Processing Steps | Human Resource Steps |
| SLI9docs | I-9 Documents | I9 Documents |
| SLInsAges | Insurance - Price per 1000 tab | Insurance Ages |
| SLInsHcs | Insurance - Coverage Classes | Coverage Classes |
| SLInsurances | Insurance | Insurances |
| SLMemoTopics | Memo Topics | Memo Topics |
| SLMilitaries | Military Service | Militaries |
| SLOffices | Offices | Offices |
| SLOrgCpnys | Companies | Companies |
| SLPlanRas | Reimbursement Plan | Reimbursement Plans |
| SLPosChgs | Position Change Reasons | Position Changes |
| SLPosClasss | Position Classifications | Position Classifications |
| SLPosDets | Positions - grid | Departmen Positions |
| SLPositions | Positions - grid | Positions |
| SLPosRqmts | Position Requiremenst | Position Requirements |
| SLPrbanks | Direct Deposit Banks | Payroll Banks |
| SLPrdecds | Deduction and Earning Codes | Payroll Deduction And Earning Codes |
| SLPrHrss | Payroll Hours | Payroll Hours |
| SLPrLogs | Payroll Log Hours for Pay Period | Payroll Logs |
| SLPrparms | Payroll Parameters | Payroll Parameters |
| SLPrtaxts | Tax Codes Exempt and W2 State FIPS Number Entry | Payroll Tax Types |
| SLPrtrxds | Payroll Distribution | Payroll Transaction Details |
| SLPrtrxps | Delete Payroll Transactions and W2 Mag Media Electronic Filing | Payroll Transaction Pays |
| SLPrtrxs | Payroll Processing and Related Utilities |  |
| SLReviews | Review Types | Reviews |
| SLSalChgs | Salary Change Reasons | Salary Changes |
| SLSicklves | Employee Sick Leave | Sick Leaves |
| SLSkills | Skills | Skills |
| SLSlparms | Sick Leave Parameters | oSlparms |
| SLTerminations | Termination Reasons | Termination Reasons |
| SLTrainings | Applicant or Employee Training Courses | Trainings |
| SLVacations | Employee Vacation | Vacations |
| SLVacParms | Vacation Parameters | Vacation Parameters |
| SLW2TaxConss | W-2 States To Be Consolidated | W2 Tax Consolidations |
| SLWantAds | Want Ads | Want Ads |
| SLWaPoses | Want Ads - grid | Want Ad Positions |
| SLWaUsage | Want Ad Usage | WaNT Usage |

### ExtFin (7 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLExportApTrxds | External Financial Interface - Export A/P Transaction Details | Export AP Transaction Details |
| SLExportApTrxs | External Financial Interface - Export A/P Transactions | Export AP Transactions |
| SLExportArInvds | External Financial Interface - Export A/R Transaction Details | Export AR Invoice Details |
| SLExportArInvs | External Financial Interface - Export A/R Transactions | Export AR Invoices |
| SLExportArTermsDues | AR terms Due records when an invoice has multiple due dates | Export Account Receive Terms Dues |
| SLExtfinParms | External Financial Interface Parameters | External Financial Parameters |
| SLTmpExportExtfinBatches | External Financial Interface - Temporary Export External Financial Batches | Temporary Export External Financial Batches |

### Finance (69 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAnaLedgers | Analytical Ledger | Analytical Ledgers |
| SLARPaymentImportMappings | AR Payment Import Map | oSLARPaymentImportMappings |
| SLArpmtImportMapGroups | AR Payment Import Map Group | AR Payment Import Map Groups |
| SLBankAddrs | Bank Address | Bank Addresses |
| SLBankHdrs | Bank Codes; Bank Account Revaluation Utility | Bank Headers |
| SLBankReconciliationUtility | IDO for automatic bank reconciliation process | obank_stmt_unreconciled_transactions |
| SLChartAlls | Chart of Accounts All | Chart Alls |
| SLChartBps | Chart of Accounts Budget and Plan | Chart Budget And Plans |
| SLChartDs | Chart of Account Allocations | Chart Details |
| SLCharts | Chart of Accounts and Related Forms/Utilities | Charts |
| SLChartTaxInfos | Chart Tax Info | oSLChartTaxInfos |
| SLChartUnitcd1_Alls | Unit Code 1 tab on Chart of Accounts - All | Chart Unit Code1 Alls |
| SLChartUnitcd1s | Unit Code 1 tab on Chart of Accounts | Chart Unit Code1s |
| SLChartUnitcd2_Alls | Unit Code 2 tab on Chart of Accounts - All | Chart Unit Code2  Alls |
| SLChartUnitcd2s | Unit Code 2 tab on Chart of Accounts | Chart Unit Code2s |
| SLChartUnitcd3_Alls | Unit Code 3 tab on Chart of Accounts - All | Chart Unit Code3  Alls |
| SLChartUnitcd3s | Unit Code 3 tab on Chart of Accounts | Chart Unit Code3s |
| SLChartUnitcd4_Alls | Unit Code 4 tab on Chart of Accounts - All | Chart Unit Code4 Alls |
| SLChartUnitcd4s | Unit Code 4 tab on Chart of Accounts | Chart Unit Code4s |
| SLCustdrfts | A/R Draft-related Forms | Customer Drafts |
| SLDraftTypes | Draft Types Form | Draft Types |
| SLFaCosts | Fixed Asset Costs | Fixed Asset Costs |
| SLFaDeprs | Fixed Asset Depreciation | Fixed Asset Depreciations |
| SLFadeptabs | Fixed Asset Depreciation Tables | Fixed Asset Depreciation Tables |
| SLFaDisps | Fixed Asset Disposal | Fixed Asset Disposals |
| SLFaDists | Fixed Asset Disposal Distributions | Fixed Asset Distributions |
| SLFamasters | Fixed Assets | Fixed Asset Masters |
| SLFaparms | Fixed Asset Parameters | Fixed Asset Parameters |
| SLFaTrans | Fixed Asset Transfer | Fixed Asset Transactions |
| SLFinanceHubAP | IDO for Finance hub AP | oSLFinanceHubAP |
| SLFinanceHubAR | IDO for Finance hub AR | SL Finance Hub A/R |
| SLFingroups | Financial Statement Groups | Financial Groups |
| SLFinTargetGroupAccounts | Target Group Accounts | ofin_target_group_accounts |
| SLFinTargetGroupActualDetails | Target Group Actual Details | ofin_target_group_actual_details |
| SLFinTargetGroupHistoricalRun | Fin Target Group Historical Run | ofin_target_group_historical_runs |
| SLFinTargetGroups | Target Groups | ofin_target_groups |
| SLFinTargetGroupTypes | Target Group Types | ofin_target_group_types |
| SLFiscalRptSystems | Fiscal Reporting Systems | Fiscal Reporting Systems |
| SLFiscalRptSystemTypes | Fiscal Reporting System Types | oFiscalRptSystemTypes |
| SLFsbJournals | FsbJournals | oFsbJournals |
| SLFsbPeriods | Multi-FSB Accounting Periods | ofsb_periods_msts |
| SLFsbs | Financial Set of Books | oFsbs |
| SLGlbanks | Bank Transaction Information for Reconciliation and Voiding Posted Payments | Global Banks |
| SLGlrpthcs | Financial Statement Definition Columns | Global Report Header Columns |
| SLGlrpths | Financial Statement Definition and Preview | Global Report Headers |
| SLGlrptlAlls | Financial Statements | Global Report Line Alls |
| SLGlrptlcs | Financial Statement Line Definition | Global Report Line Columns |
| SLGlrptls | Financial Statement Preview - grid | Global Report Lines |
| SLGlrptlss | Financial Statement Line Definition - grid on Total tab | Global Report Line Sequences |
| SLJournals | Journals | Journal Entrys |
| SLLedgerAlls | G/L Posted Transactions | Ledger Alls |
| SLLedgers | G/L Posted Transactions | Ledgers |
| SLPeriods | Accounting Periods | Periods |
| SLPeriodsSeqs | Accounting Period Control Number Sequences | Periods Sequences |
| SLPerSorts | Period Sorting Methods | Period Sorting |
| SLPertots | Handles per-tot table data for several utilities | Period Totals |
| SLPositivePayFormatFields | Positive Pay Format Fields | Positive Pay Format Fields |
| SLPositivePayFormatSections | Positive Pay Format Section | Positive Pay Format Sections |
| SLTTFinstmts | Temporary Table tt_finstmt | Temporary Table Finance Statements |
| SLTTJournals | IDO for manipulating tt-journal with MassJournalPosting | Temporary Table Journals |
| SLUnitcd1Alls | Unit Code 1 All | Unit Code1 Alls |
| SLUnitcd1s | Unit Code 1 | Unit Code1s |
| SLUnitcd2Alls | Unit Code 2 All | Unit Code2 Alls |
| SLUnitcd2s | Unit Code 2 | Unit Code2s |
| SLUnitcd3Alls | Unit Code 3 All | Unit Code3 Alls |
| SLUnitcd3s | Unit Code 3 | Unit Code3s |
| SLUnitcd4Alls | Unit Code 4 All | Unit Code4 Alls |
| SLUnitcd4s | Unit Code 4 | Unit Code4s |
| SLVatObligations | MTD | oSLVatObligations |

### FSPlusUnit (1 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLPortalFSUnits | IDO created for SyteLine Portals |  |

### Material (115 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLBolItems | Advance Ship Notice Line Items | Bill of Lading Items |
| SLBols | Advance Ship Notices | Bill of Ladings |
| SLCompliancePrograms | Compliance Programs | oCompliancePrograms |
| SLContainerItems | Container Item | Container Items |
| SLContainers | Container | Containers |
| SLCostingAltCompareCostingAltItems | Costing Alternative Compare Costing Alt Items | Costing Alt Compare Costing Alt Items |
| SLCostingAltCompareItems | Costing Alternative Compare Items | Costing Alt Compare Items |
| SLCostingAltCompareItemWhses | Costing Alternative Compare Item Whses | Costing Alt Compare Item Whses |
| SLCostingAltDepts | Costing Alternative Departments | oCostingAltDepts |
| SLCostingAltItems | Costing Alternative Items | oCostingAltItems |
| SLCostingAltMaterials | Costing Alternative Materials | Costing Alternative Materials |
| SLCostingAltProductCodes | Costing Alternative Product Codes | oCostingAltProductCodes |
| SLCostingAlts | Costing Alternative | oCostingAlts |
| SLCostingAltWcs | Costing Alternative Wcs | oCostingAltWcs |
| SLCustomerPortalItems | IDO used only by the customer portal | Customer Portal Items |
| SLCycles | Cycle Count Posting & Update | Cycles |
| SLDocProfileMaterial | Pro Forma Invoice Report | Document Profile Material |
| SLEcndists | ECN Distribution Codes | Engineering Change Notice Distributions |
| SLEcnhitems | History Engineering Change Notice Items | Engineering Change Notice History Items |
| SLecnhs | History Engineering Change Notices | Engineering Change Notice Histories |
| SLEcnitems | Engineering Change Notice Items | Engineering Change Notice Items |
| SLEcnpris | ECN Priority Codes | Engineering Change Notice Priorities |
| SLEcns | Engineering Change Notices | Engineering Change Notice |
| SLEdiVsnLotSerials | Collection of Lot/Serial number records for inbound EDI Vendor Shipments | EDI Vendor Shipment Lot Serials |
| SLEngineeringNPDCodes | Engineering NPD Codes | Engineering NPD Codes |
| SLFamCodes | Family Codes | Family Codes |
| SLFeatItems | Feature Group Ranks | Feature Items |
| SLFeatranks | Feature Group Re-ranks | Feature Ranks |
| SLFeatures | Feature Groups | Features |
| SLForecasts | Forecast | Forecasts |
| SLIntraSiteTransferDetails | SLIntraSiteTransferDetails | Intra Site Transfer Details |
| SLIntraSiteTransferSupDems | SLIntraSiteTransferSupDems | Intra Site Transfers |
| SLIntraSiteTransferWhses | Distribution Warehouses | Intra Site Transfer Warehouses |
| SLInvparms | Inventory Parameters and Transfer Order Parameters | Inventory Parameters |
| SLItemacts | Miscellaneous Issue, Quantity Adjustment, or Manual LIFO/FIFO Adjustment | Item Acts |
| SLItemAlls | Items All | Item Alls |
| SLItemCategories | IDO for Item Catagories | Item Categories |
| SLItemCategoryItems | IDO for Item Category Items | Item Category Items |
| SLItemCategoryLangs | IDO for Item Catatory Language | Item Category Languages |
| SLItemGlbls | Global Items | Item Globals |
| SLItemLangs | Multi-Lingual Item | Item Languages |
| SLItemLifos | Item Lifo Fifo Stack | Item Lifos |
| SLItemlocAlls | Item Stockroom Locations All | Item Location Alls |
| SLItemLocs | Item Stockroom Locations and Related Utilities | Item Locations |
| SLItemprices | Item Pricing or Change Item Price | Item Prices |
| SLItemrevs | Delete Item Revision | Item Revision |
| SLItems | Item master | Items |
| SLItemsNonInventoryItems | Listed Items and Non-Inventory Items | oSLItemsNonInventoryItems |
| SLItemwhses | Item Warehouses, Item Initialization, and Set YTD/PTD to Zero | Items |
| SLLocationAlls | Locations All | Location Alls |
| SLLocations | Locations | Locations |
| SLLotAlls | Lots All | Lot Alls |
| SLLotLocAlls | Item Lot Locations All | Lot Location Alls |
| SLLotLocs | Item Lot Locations | Item Lot Locations |
| SLLots | Lots and Delete Lots | Lots |
| SLManufacturerItems | Manufacturer Items | Manufacturer Items |
| SLMatltranAlls | Posted Transaction and Delete Material Transactions | oMatltranAlls |
| SLMatltranAmts | Posted Transaction - Grid | Material Transaction Amounts |
| SLMatltrans | Posted Transaction and Delete Material Transactions | Material Transactions |
| SLMrpWbs | Material Planner Workbench and Related Utilities | Mrp Workbenchs |
| SLMSMoves | Multi-Site Quantity Move | Multi-Site Moves |
| SLMSSerials | Multi-Site Quantity Move - Serial Numbers tab grid | Multi-Site Serials |
| SLNonInventoryItems | Non Inventory Items | oSLNonInventoryItems |
| SLPeggingDisplays | Pegging Display | Pegging Displays |
| SLPhyinvs | Used for Physical Inventory Error Processing | Physical Inventories |
| SLPhytags | Set Tag Sheet Controls | Physical Tags |
| SLPlanningDetails | Planning Detail and Related Forms | Planning Details |
| SLPlants | Plants | oPlants |
| SLPlnSupplySourceRuleDtls | Supply Source Rule Details | oPlnSupplySourceRuleDtls |
| SLPlnSupplySourceRules | Supply Source Rules | oPlnSupplySourceRules |
| SLPlnSupplySrcRuleDtls | Supply Source Rule Details | Supply Source Rule Details |
| SLPlnSupplySrcRules | Supply Source Rules | Supply Source Rules |
| SLPortalInventory | Created for the CP Inventory web page | oInventory |
| SLPortalProducts_H_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HC_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HCD_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HCDI_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HCI_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HD_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HDI_Views | Portal Products View | oPortalProductsViews |
| SLPortalProducts_HI_Views | Portal Products View | oPortalProductsViews |
| SLPortalProductsViews | Portal Products View | oPortalProductsViews |
| SLPricecodeAlls | Price Codes All | Pricecode Alls |
| SLPricecodes | Price Codes | Price Codes |
| SLProdMixes | Co-Product Mix | Product Mixes |
| SLProdMixIrts | Co-Product Mix Operations | Co-Product Mix Operations |
| SLProdMixItems | Co-Product Mix - Grid | Product Mix Items |
| SLQualifierStrings | Feature Group Qualifiers | Qualifier Strings |
| SLRcpts | Master Production Schedule and Related Utilities | Receipts |
| SLRelatedItems | IDO for Related Items | Related Items |
| SLRsvdInvAlls | Reservations for Item or Reservations for Order | Reservations |
| SLRsvdInvs | Reservations for Item or Reservations for Order | Reservations |
| SLSerialAlls | Serial Numbers, Delete Serials, or Post Job WIP Move Transactions | Serial Numbers |
| SLSerials | Serial Numbers, Delete Serials, or Post Job WIP Move Transactions | Serial Numbers |
| SLSitenets | Inter-Site Parameters | Site Nets |
| SLStockActItems | Miscellaneous Receipt | Stockroom Activity Items |
| SLSupDems | SLSupDems IDO | Sup Dems |
| SLTaxFreeExports | Tax Free Exports | Tax Free Exports |
| SLTaxFreeImportItems | Tax Free Import Items | Tax Free Import Items |
| SLTaxFreeImports | Tax Free Imports | Tax Free Imports |
| SLTmpForecastImport | IDO used for bulk import of forecast data | otmp_forecast_imports |
| SLTmpMsgBuffers | for using temporary message buffer | Temporary Message Buffers |
| SLTransferAlls | Transfer Orders and Related Utilities | Transfer Alls |
| SLTransfers | Transfer Orders and Related Utilities | Transfers |
| SLTrnacts | Transfer Order Ship, Transfer Order Receive, and Combined TO Ship/Receive | Transfer Acts |
| SLTrnitemAlls | Transfer Order Line Items and Related Utilities | Transfer Items |
| SLTrnitems | Transfer Order Line Items and Related Utilities | Transfer Items |
| SLTrpHdrs | Generate From Packing Slip | Transfer Pack Headers |
| SLTrxRestrictCodeAlls | Transaction Restriction Code All | Transaction Restriction Code Alls |
| SLVendConsignmentWhseItems | Inventory Consigned From Vendor Receipt | Vendor Consignment Whse Items |
| SLVendorPortalItems | IDO used only by the Vendor Portal | Vendor Portal Items |
| SLWhseAllRepRules | Whse All For Replication Rules | Whse All For Replication Rules |
| SLWhseAlls | Warehouses All | Warehouse Alls |
| SLWhses | Warehouses | Warehouses |
| SLWhseTransitTimes | Warehouse Transit Times | owhse_transit_times |

### MGCore (16 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLHighKeys | View of NextKeys table without duplicates or non-high values | High Keys |
| SLIntranets | Intranets | Intranets |
| SLJobQueues | Job Queue Information | Job Queue Information |
| SLRepCategories | Replication Categories | Replication Categories |
| SLReplicationTriggers | Code to generate replication triggers. | Replication Triggers |
| SLRepObjectCategories | Replication Categories - grid | Replication Categories |
| SLRepRules | Replication rules | Replication Rules |
| SLRptOpts | Report Options Table | Report Options |
| SLRptOptValues | Report Option Values by userid | Report Option Values |
| SLShadowValues | Multi-site replication data table. | Replication Data |
| SLShadowValuesErrors | Inbound replication errors. | Inbound Replication Errors |
| SLSiteGroups | Site Groups | Site Groups |
| SLSiteLinkInfos | Sites/Entities - Link Info tab | Site Link Infos |
| SLSites | Sites/Entities | Sites |
| SLSiteUserMaps | User ids to use when logging in for replication. | Site User Maps |
| SLSystemTypes | System Types | System Types |

### Mobile (10 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLMobileDeleteTrackings | Delete Tracking for mobile updates | omobile_delete_trackings |
| SLMobileDeviceChildIDOs | Child IDOs on mobile device | omobile_device_child_ido_msts |
| SLMobileDeviceDatas | Mobile Device Synchronization Data | omobile_device_datas |
| SLMobileDeviceFields | Custom Mobile Fields | omobile_device_fields |
| SLMobileDeviceGroups | Groups allowed to acess the Mobile Ext. | omobile_device_groups |
| SLMobileDeviceIDOFilters | Row Filters for Mobile IDOs | omobile_device_ido_filters |
| SLMobileDeviceIDOLinks | Parent/Child IDO Link on Mobile | omobile_device_ido_link_msts |
| SLMobileDeviceIDOs | IDO Collections to use on mobile | omobile_device_ido_msts |
| SLMobileDeviceUsers | Users allowed to access the Mobile Ext. | omobile_device_users |
| SLMobileParms | Mobile Parameters | omobile_parms |

### NonTrans (1 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLNonTrans | IDO for methods that can't run in the context of a transaction, but have not yet been moved to a better place (obsolescent) | Non Transactions |

### PLLOC (13 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLPLInvKSeFMarkingAlls | Invoice KSeF Marking Alls | Invoice KSeF Marking Alls |
| SLPLInvKSeFMarkings | Poland Invoice KSeF Markings | Invoice KSeF Marking |
| SLPLKSeFCertificates | Poland KSeF Certificates | KSeF Certificates |
| SLPLKSeFLogs | KSeF API Logs | KSeF Logs |
| SLPLKSeFMarkings | Marking ID for Poland KSeF E-Invoicing | Markings |
| SLPLKSeFParms | Parameters for Poland KSeF E-Invoicing | KSeF Parameters |
| SLPLKSeFUsers | User configuration for Poland KSeF E-Invoicing | KSeF Users |
| SLPLProFormaInvHdrs | Pro Forma Invoice Headers | Pro Forma Invoice Headers |
| SLPLProFormaInvItems | Pro Forma Invoice Lines | Pro Forma Invoice Lines |
| SLPLStaxAccepts | Poland Tax Acceptance IDO | oSLPLStaxAccepts |
| SLPLTurnoverBalances | Turnover and Balances | Journal Entrys |
| SLPLVATWhiteListParms | Parameters and methods for verifying the status of VAT/VIES/GUS taxpayers | Poland VAT White List Parameters |
| SLPLVendorWhiteListCheckLog | PL Vendor White List Check Logs | oSLPLVendorWhiteListCheckLog |

### Product (74 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAltscheds | Bound to ALTSCHED, an APS table | Alternate schedules |
| SLAppcfgs | Not used | Application Configurations |
| SLBatch | Batched Productions | Batch |
| SLBATCH000s | Batch Definitions | Batches |
| SLBatchProd | Batched Production Operations | Batch Prod |
| SLBatchProdRoutes | Batched Production Routes | Batch  Production Routes |
| SLBatchRoutes | Batch Routes | Batch Routes |
| SLBatchTime | Batch Times | Batch Time |
| SLBatchWait | Batch Waits | Batch Wait |
| SLBomListing | Routing BOM Listing | BOM Listing |
| SLCAL000s | Holidays | Holidays |
| SLIndcodes | Indirect Labor Codes | Ind Codes |
| SLJobacts | Jobacts IDO | Job Activities |
| SLJobAlls | Job Orders for All Site Group | Job Alls |
| SLJobCoitems | Estimation Worksheet | Job Customer Order Items |
| SLJobitems | Co-Product Job Orders | Job Items |
| SLJobMatlAlls | Job Materials for All Site Group | Job Material Alls |
| SLJobmatlCompliances | Job Materials Compliances | Job Materials |
| SLJobmatlJobs | Job Materials - Cross References to Jobs | Job Material Jobs |
| SLJobmatlPos | Jobmatl cross references to purchase orders (where used) | Job Material Purchase Orders |
| SLJobmatlReqs | Job Materials - Cross References to Requisitions | Job Material Requsitions |
| SLJobmatls | Jobmatl IDO | Job Materials |
| SLJobmatlTrns | Job Materials - Cross References to Transfer Orders | Job Material Transfers |
| SLJobPriceBreaks | Job Price Break | Job Price Break |
| SLJobRefs | Job Material References | Job References |
| SLJobRouteAlls | Jobroute IDO for All Sites | Job Route Alls |
| SLJobRoutes | Jobroute IDO | Job Routes |
| SLJobs | Job Orders and related forms | Jobs |
| SLJobSchs | Job Schedule | Job Schedules |
| SLJobtCls | Pending Job Labor Transactions | Pending Job Labor Transactions |
| SLJobtMats | Pending Material Transactions | Jobt Materials |
| SLJobTranAlls | Job Transaction for All Site Group | Job Transaction Alls |
| SLJobtranitems | Unposted Job Transactions - Co-products Grid | Job  Transaction Items |
| SLJobTrans | Job Transaction-related Forms | Job  Transactions |
| SLJobtSers | Pending Serial Transactions | Job Transaction Serials |
| SLJrtItems | Job Operations - Co-products tab | Job Route Items |
| SLJrtResourceGroups | Resource grid on Job Operations and Related Forms | Job Route Resource Groups |
| SLJrtSchs | Jobroute Schedule records | Job Route  Schedules |
| SLJsattr000s | Bound to JSATTR, an APS input table that contains operation attribute values | Job Schedule Attributes |
| SLMachineSetupTimeVariance | Machine Setup Time | oMachineSetupTimeVarianceViews |
| SLMaterialListing | Routing BOM Listing - Grid | Material Listing |
| SLMrpExcs | Exception Message Priorities | MRP Exceptions |
| SLMrpParms | Planning Parameters | MRP Parameters |
| SLPickMachByWcs | Allows the Machine browser to only show Machine Resource IDs associated with the entered Work Centers that have been released to the Production Floor | Pick Machine By Work Centers |
| SLPItems | Production Schedule Items | Production Items |
| SLPlanint000s | Resource Planning Intervals | Planning Intervals |
| SLProductionHubAP | Production Hub All Production | oProductionHubAllProduction |
| SLProductionPlannerViews | Production Planner Home | Production Planner Views |
| SLPs | 2 | Production Schedule |
| SLPsitems | Production Schedule Items | Production Schedule Items |
| SLRbwsPm | RBWS Production Manager Workspace | oRBWSProduction anagerWorkspace |
| SLResattr000s | Bound to RESATTR, an APS input table that contains resource attribute values | Resource Attributes |
| SLResGrps | Where Used Resource Groups | Resource Groups |
| SLResourceSchedSortCols | Resource Schedules Sort Columns | oResourceSchedSortCols |
| SLResourceTypes | Resource Type | Resource Types |
| SLResrc000s | Resources | Resources |
| SLResRefs | Where Used Resources | Resource References |
| SLResschd000s | Resource Sequencing Or Resource Group Sequencing | Resource Schedules |
| SLRgattr000s | Bound to RGATTR, an APS input table that contains resource group attribute values | Resource Group Attributes |
| SLRgrp000s | Resource Groups | Resource Groups |
| SLRgrpItems | Where Used Resource Groups - Items | Resource Group Items |
| SLRgrpJobs | Where Used Resource Groups - Jobs | Resource Group Jobs |
| SLRgrpmbr000s | Resource Groups - Resources tab | Resource Group Members |
| SLRgrpRefs | Where Used Resource Groups | Resource Group References |
| SLRgrpWcs | Where Used Resource Groups - Work Centers | Resource Group Work Centers |
| SLSepAttrib | Separation Attributes | Separation Attributes |
| SLSetupGroups | Setup Groups | Setup Groups |
| SLSfcparms | Shop Floor Control Parameters | Shop Floor Control Parameters |
| SLShift000s | Scheduling Shifts | Shifts |
| SLShiftexdi000s | Resources - Shift Exceptions Tab | Shift Exceptions |
| SLTmpJobSplits | Job Lot Splitting | Temporary Job Splits |
| SLTtJobtMatPosts | Pending Job Material Transaction Posting | Temporary Table Job Transaction Material Posts |
| SLWcResourceGroups | Job Operations - Co-products tab | Resource Groups |
| SLWcs | Work Centers | Work Centers |

### Projects (34 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLInvMs | Invoice Milestones and Related Forms | Invoice Milestones |
| SLInvMsLogs | Audit Tab on Invoice Milestones and Related Forms | Invoice Milestone Logs |
| SLInvMsSeqs | Requirements Tab on Invoice Milestones and Related Forms | Invoice Milestone Sequences |
| SLProjAlls | Projects All | Projects All |
| SLProjBolItems | Project ASNs | Project Bill of Lading Items |
| SLProjBols | Project Advance Ship Notices | Project Bill of Lading |
| SLProjCostAlls | Project Cost for All Sites | Project Cost Alls |
| SLProjcostdetailAlls | Project Cost Details for All Sites | Project Cost Detail Alls |
| SLProjCosts | Project Control Cost Detail by Cost Code | Project Costs |
| SLProjectHub | Project Hub | oProjectHub |
| SLProjectHubRequisitionsSourcing | Project Hub Requisitions Sourcing | Project Hub Requisitions Sourcing |
| SLProjectHubSROsSourcing | Project Hub SROs Sourcing | Project Hub SROs Sourcing |
| SLProjectHubTransferSourcingProject | Project Hub Transfer Sourcing Project | Project Hub Transfer Sourcing Project |
| SLProjLabrs | Project Labor Transactions | Project Labors |
| SLProjMatlAlls | Project Resource for All Sites | Project Material Alls |
| SLProjMatls | Project Resources | Project Materials |
| SLProjParms | Project Parameters | Project Parameters |
| SLProjPckHdrs | Project Packing Slip and Related Forms | Project Packing Headers |
| SLProjs | Projects | Projects |
| SLProjShips | Project Resources - Shipping Tab | Project Ships |
| SLProjTaskAlls | Project Tasks for All Site | Project Task Alls |
| SLProjTasks | Project Tasks and Related Forms | Project Tasks |
| SLProjTranAlls | Project Transactions for All Sites | Project Transaction Alls |
| SLProjWipAdjViews | data source for Project Wip Adjustments form | Project Wip Adjustment Views |
| SLProjWorkResources | Project Work Resources eg. User, Employee, Vendor etc... | Project Work Resources |
| SLRevMs | Revenue Milestones and Related Forms | Revenue Milestones |
| SLRevMsLogs | Audit Tab on Revenue Milestones and Related Forms | Revenue Milestones Logs |
| SLRevMsSeqs | Requirements Tab on Revenue Milestones and Related Forms | Revenue Milestones Sequences |
| SLUnPostedTransactionsViews | UnPosted transaction tables row count | Un Posted Transactions Views |
| SLWBSAlls | Work Breakdown Structures for All Sites | Work Breakdown Structure Alls |
| SLWBSItemAlls | Work Breakdown Structures - Items Tab for All Sites | Work Breakdown Structure Item Alls |
| SLWBSItems | Work Breakdown Structures - Items Tab | Work Breakdown Structure Items |
| SLWBSs | Work Breakdown Structures | Work Breakdown Structures |
| SLWBSViews | Used by WBS Tree View - recursively | Work Breakdown Structure Views |

### Report (26 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLAmortizationOutstandingReport | Amortization Outstanding Report | oSLAmortizationOutstandingReport |
| SLFixedAssetMovementDetailReport | Fixed Asset Movement Detail Report | Fixed Asset Movement Detail Report |
| SLFixedAssetMovementReport | Fixed Asset Movement Report | Fixed Asset Movement Report |
| SLGeneralLedgerTransactionS01DNReport | General Ledger Transaction S01DN Report | sGeneralLedgerTransactionS01DNReport |
| SLGeneralLedgerTransactionS03aDNReport | General Ledger Transaction S03aDN Report | sGeneralLedgerTransactionS03aDNReport |
| SLGLVoucherReport | oGLVoucherReport | oGLVoucherReport |
| SLJournalCompressReport | Journal Compress Report | SLJournal Compress Report |
| SLJournalControlNumberReport | Journal Control Number Report | oSLJournalControlNumberReport |
| SLJournalTransactionReport | oJournalTransactionReport | oJournalTransactionReport |
| SLMasterPlanningReport | Master Planning Report | oSLMasterPlanningReport |
| SLMXCFDIReport | Mexico CFDI Report | CFDI Report |
| SLPLARAPReportsforaDay | AR AP Report for a Day Accounts | AR/AP Reports for a Day |
| SLPLARAPSettlementAsOfDayReport | Poland AR-AP Settlement As of Day Report | Poland AR-AP Settlement As of Day Report |
| SLPLInventoryAsOfDayReport |  | Poland Inventory As of Day Report |
| SLPLInventoryForADayReport |  | Poland Inventory For A Day Report |
| SLPLOrderProFormaInvoiceReport | Order Pro Forma Invoice Report | Order Pro Forma Invoice Report |
| SLPLPOReceivingSettlementReport | PO Receiving Settlement | PO Receiving Settlement Report |
| SLPLProjectWIPAsOfDayReport | Project WIP As Of Day Report | Project WIP As of Day Report |
| SLPLProjectWIPForADayReport | Project WIP For A Day Report | Project WIP For A Day Report |
| SLPLTurnoverBalancesReport | Turnover and Balances Report | Journal Entrys |
| SLPurchaseVATRegister012GTGT | Format for Vietnam localization |  |
| SLRebalanceCustomerBalancesMessageReport | Rebalance Customer Balances Message Rpt | Rebalance Customer Balances Message Report |
| SLResourceGroupDispatchListReport | Resource Group Dispatch List Report | Resource Group Dispatch List Report |
| SLSalesVATRegister011GTGT | Format for Vietnam Localization | Sales VAT Register 01-1/GTGT Report |
| SLYearToDateDeductionsandEarnings | DataView for YearToDateDeductionsandEarnings | oSLYearToDateDeductionsandEarnings |
| SLYearToDateDeductionsAndEarningsReport | DataView for YearToDateDeductionsandEarnings | oSLYearToDateDeductionsAndEarningsReport |

### Vendor (82 IDOs)

| IDO Name | Description | Caption |
|----------|-------------|---------|
| SLApdraftts | Draft Remittance | AP Draft Remittances |
| SLApParms | Accounts Payable Parameters | Account Payable Parameters |
| SLApPayDisVchs | Outstanding Vouchers for Payment Distributions | Account Payable Pay Distribution Vouchers |
| SLAppmtds | A/P Payment Distribution and A/P Payment Generation | AP Payment Distributions |
| SLAppmts | A/P Payments and A/P Posting Forms | Account Payable Payments |
| SLAptrxds | A/P Transaction Distributions | Account Payable Transaction Distributions |
| SLAptrxpAlls | A/P Posted Transaction - All | Account Payable Posted Transactions Alls |
| SLAptrxps | A/P Posted Transaction | Account Payable Posted Transactions |
| SLAptrxrs | Aptrxr Table | AP Transactions |
| SLAptrxs | A/P Vouchers and Adjustments and Voucher Authorization | AP Transactions |
| SLAptxrds | Recurring Voucher Distribution | AP Transaction Details |
| SLBankFileFmts | Bank File Formats | Bank File Formats |
| SLBankHdrsAlls | Bank Address - All | Bank Header Alls |
| SLCommodities | Commodity Codes | Commodity Codes |
| SLCurrencyAlls | Currency Codes - All | Currency Alls |
| SLDocProfileVendors | Vendor Document Profile and PO Reports | Document Profile Vendors |
| SLEdiPoAckBlns | EDI Purchase Order Acknowledgement Blanket Lines/Releases | EDI Purchase Order Acknowledgement Blanket |
| SLEdiPoAckItems | EDI Purchase Order Acknowledgement Lines | EDI Purchase Order Acknowledgement Items |
| SLEdiPoAcks | EDI Purchase Order Acknowledgements | EDI Purchase Order Acknowledgements |
| SLEdiPoitems | Collection of outbound EDI Purchase Order Line Items | EDI Purchase Order Items |
| SLEdiPos | Retransmit EDI POs and Ship Schedules | EDI Purchase Orders |
| SLEdiScheds | Retransmit EDI Planning Schedules | EDI Schedules |
| SLEdiVinvs | Collection of inbound EDI Vendor Invoice Headers. Runs purge process on Purge EDI Vendor Invoices | EDI Vendor Invoices |
| SLGenAPTrans | Supports form Generate A/P Transactions | Generate Account Payable Transactions |
| SLGenAPTransFilterString | Supports form Generate A/P Transactions | Generate Account Payable Transactions |
| SLGrnHdrs | Goods Receiving Notes and Related Forms | Goods Receiving Note Headers |
| SLGrnLines | Goods Receiving Notes Lines | Goods Receiving Notes Lines |
| SLItemVendPriceAlls | Item Vendor Cross Reference Prices | Item Vendor Prices Alls |
| SLItemVendPrices | Item Vendor Cross Reference Prices | Item Vendor Prices |
| SLItemvends | Item/Vendor Cross References | Item Vendors |
| SLLcRcpts | Generate Landed Cost Vouchers | Landed Cost Receipts |
| SLParmsAlls | General Parameters - All | Parameters Alls |
| SLPitemhs | History Purchase Order Lines and History PO Blanket Line/Releases | Purchase Order Item Histories |
| SLPoAlls | Purchase Orders All | Purchase Order Alls |
| SLPoBlnhs | History PO Blanket Lines | Purchase Order Blanket Line Histories |
| SLPoBlns | Purchase Order Blanket Lines | Purchase Order Blanket Lines |
| SLPochanges | PO Change Orders | Purchase Order changes |
| SLPohs |  | Purchase Order Histories |
| SLPoItemAlls | PO Blanket Releases and Related Forms - All | Purchase Order Item Alls |
| SLPoitemLogs | Purchase Order Lines Change Log | Purchase Order Lines Logs |
| SLPoItems | PO Blanket Releases and Related Forms | Purchase Order Items |
| SLPoItmchgs | PO Change Orders - Grid | Purchase Order Changes |
| SLPoLangs | Purchase Order Language Translations | Purchase Order Languages |
| SLPOMissingInformationViews | Purchase Orders Missing Information | Purchase Orders Missing Information Views |
| SLPoparms | Purchasing Parameters | Purchase Order Parameters |
| SLPoRcpts | Purchase Order Receipts or History PO Receipts | Purchase Order Receipts |
| SLPos | Purchase Orders and a lot of related forms | Purchase Orders |
| SLPreqcodes | Purchase Order Requisition Codes | Purchase Order Requisition Codes |
| SLPreqitems | Purchase Order Requisition Lines | Purchase Order Requisition Items |
| SLPreqs | Purchase Order Requisitions | Purchase Order Requisitions |
| SLSupEdiParms | Supply EDI Parameters - Interface Setup | Supply EDI Parameters |
| SLTermsAlls | IDO on termsl_all table | Terms Alls |
| SLTmpLCTaxDists | Supports the Taxes tab subcollection on the Generate Landed Cost Vouchers form | Temporary Landed Cost Tax Distributions |
| SLTmpPoBuilders | Handles the temp table for PO Builder | Temporary Purchase Order Builders |
| SLTmpVoucherBuilders | Handles the temp table for Voucher Builder | Temporary Voucher Builders |
| SLTransNature2Alls | Secondary Nature of Transaction Codes - All | Transaction Nature Secondary Alls |
| SLTTApPosts | A/P Voucher Posting | Temporary Table Account Payment Posts |
| SLTTGlBanks | Void Posted Draft Payments | Temporary Table Global Banks |
| SLTTVouchers | Permanent version of tt-voucher temp table (key includes connection_id) | Temporary Table Vouchers |
| SLTTVouchersFilterString | Permanent version of tt-voucher temp table (key includes connection_id) | Temporary Table Vouchers |
| SLVchHdrs | Purge Voucher History | Voucher Headers |
| SLVchItemAlls | Voucher Listing | Voucher Item Alls |
| SLVchPrAlls | Posted Transaction - Voucher Pre-register | Voucher Pre-register Alls |
| SLVchPRs | Vouchers Pre-Register | Vouchers Pre-Register |
| SLVchPrStaxAlls | Voucher Pre-register Tax Distributions All | Voucher Payroll Sale Tax Alls |
| SLVchPrStaxs | Voucher Pre-register Tax Distributions | Voucher Payroll Sale Taxs |
| SLVchStaxs | vch_stax table information. Create for IDO Report. | Voucher Sale Taxs |
| SLVendaddrs | Vendaddr table information | Vendor Addresses |
| SLVendcatAlls | Vendor Categories - All | Vendor Category Alls |
| SLVendCats | Vendor Categories | Vendor Categories |
| SLVendLcrs | Vendor Letters of Credit and Related Forms | Vendor Letters |
| SLVendOnTimeDelPercents | Vendor On Time Delivery information | Vendor On Time Delivery Percents |
| SLVendorAlls | Vendors and Related Forms - All | Vendor Alls |
| SLVendorCertifications | Vendor Certification | Vendor Certifications |
| SLVendorCurrencies | Vendor Currency Code | Vendor Currencies |
| SLVendorMinorityTypeAlls | Vendor Minority Type Alls | Vendor Minority Type Alls |
| SLVendorMinorityTypes | Vendor Minority Types | Vendor Minority Types |
| SLVendorPortalCompanyProfile | Created for Vendor Portal - My Company Profile web page | Vendor Portal Company Profile |
| SLVendors | Vendors and Related Forms | Vendors |
| SLVendorSurchargeRules | Vendor Surcharge Rules | oSLVendorSurchargeRules |
| SLVendorUsernames | Vendor Usernames | Vendor Usernames |
| SLVendTps | EDI Vendor Profiles | Vendor Profiles |

## Alphabetical Index

| IDO Name | Project | Description |
|----------|---------|-------------|
| SLAbsences | Employee | Absence Reasons |
| SLAccountAuthorizations | Codes | Account Authorizations |
| SLAcks | Customer | Retransmit EDI invoices, ASNs, Planning Schedules, Acknowledgements |
| SLAdpParms | Employee | ADP integration parameters |
| SLAltplans | APS | Used by the Planning Mode and Planning Parameters forms.  Bound to ALTPLAN |
| SLAltscheds | Product | Bound to ALTSCHED, an APS table |
| SLAmortizationOutstandingReport | Report | Amortization Outstanding Report |
| SLAnaLedgers | Finance | Analytical Ledger |
| SLApdraftts | Vendor | Draft Remittance |
| SLApParms | Vendor | Accounts Payable Parameters |
| SLApPayDisVchs | Vendor | Outstanding Vouchers for Payment Distributions |
| SLAppcfgs | Product | Not used |
| SLAppEds | Employee | Applicant Education |
| SLAppInts | Employee | Applicant Interviews |
| SLApplicants | Employee | Applicants |
| SLApplicationDebugLogs | Admin | Application debug message logs |
| SLApplicationModules | Admin | Date Management - List of Modules |
| SLAppmtds | Vendor | A/P Payment Distribution and A/P Payment Generation |
| SLAppmts | Vendor | A/P Payments and A/P Posting Forms |
| SLAppRefs | Employee | Applicant Reference |
| SLAppSources | Employee | Application Sources |
| SLAppWorkflows | Admin | IDO for application system event handlers. |
| SLAPSDataVisualization | APS | IDO for APS Data Visualization Hub |
| SLApsParmAlls | APS | Planning Mode Multi-Site |
| SLApsParms | APS | Planning Mode |
| SLApsplandetails | APS | Replicate planning detail to other sites when running the Planning activity in single-site mode |
| SLApsRes | APS | Used in validator - ApsResourceInColl |
| SLApsSeqs | APS | MRP-APS Order Priority |
| SLApsSites | APS | Used by the Planning Parameters form. Bound to aps_site |
| SLAptrxds | Vendor | A/P Transaction Distributions |
| SLAptrxpAlls | Vendor | A/P Posted Transaction - All |
| SLAptrxps | Vendor | A/P Posted Transaction |
| SLAptrxrs | Vendor | Aptrxr Table |
| SLAptrxs | Vendor | A/P Vouchers and Adjustments and Voucher Authorization |
| SLAptxrds | Vendor | Recurring Voucher Distribution |
| SLARCustomerBankAccounts | Customer | AR Customer bank account |
| SLARDirectDebit | Customer | A/R Direct Debit |
| SLArDraftts | Customer | Possibly used for A/R Draft Remittance, or may be obsoleted by SLCustdrfts |
| SLArEftImportArpmtds | Customer | AR Payment Distributions |
| SLArEftImportArpmts | Customer | AR Payments |
| SLArfins | Customer | Finance Charge Posting |
| SLArinvAlls | Customer | nvoices, Debit and Credit Memos All |
| SLArinvds | Customer | Invoices, Debit and Credit Memos G/L Distribution |
| SLArinvItems | Customer | For Manual Invoice Items |
| SLArinvs | Customer | Invoices, Debit and Credit Memos |
| SLArparms | Customer | Accounts Receivable Parameters |
| SLARPaymentImportConversions | Customer | A/R payment import conversions |
| SLARPaymentImportMapFields | Customer | A/R Payment Import Field Mappings |
| SLARPaymentImportMappings | Finance | AR Payment Import Map |
| SLARPaymentImports | Customer | AR Payment Imports |
| SLArpmtds | Customer | A/R Payment Distributions |
| SLArpmtImportMapGroups | Finance | AR Payment Import Map Group |
| SLArpmts | Customer | A/R Payments |
| SLArTermsDueAlls | Customer | Multiple Due Date Invoice |
| SLARTermsDues | Customer | Multiple Due Date Invoice |
| SLArtranAlls | Customer | A/R Posted Transactions All |
| SLArtrans | Customer | A/R Posted Transactions |
| SLArtranSiteAlls | Customer | A/R Posted Transactions All, it includes data from all the sites |
| SLAwards | Employee | Awards/Citations |
| SLBankAddrs | Finance | Bank Address |
| SLBankFileFmts | Vendor | Bank File Formats |
| SLBankHdrs | Finance | Bank Codes; Bank Account Revaluation Utility |
| SLBankHdrsAlls | Vendor | Bank Address - All |
| SLBankReconciliationUtility | Finance | IDO for automatic bank reconciliation process |
| SLBatch | Product | Batched Productions |
| SLBATCH000s | Product | Batch Definitions |
| SLBatchProd | Product | Batched Production Operations |
| SLBatchProdRoutes | Product | Batched Production Routes |
| SLBatchRoutes | Product | Batch Routes |
| SLBatchTime | Product | Batch Times |
| SLBatchWait | Product | Batch Waits |
| SLBolItems | Material | Advance Ship Notice Line Items |
| SLBols | Material | Advance Ship Notices |
| SLBomListing | Product | Routing BOM Listing |
| SLCAL000s | Product | Holidays |
| SLCalculators | Admin | Dummy IDO for SyteLineCalculator |
| SLCampaignCommunications | Customer | Marketing Campaign Communications |
| SLCampaignContacts | Customer | Marketing Campaign Contacts |
| SLCampaignItems | Customer | Marketing Campaign Items |
| SLCampaigns | Customer | Marketing Campaigns |
| SLCampaignStatuses | Customer | Marketing Campaign Statuses |
| SLCampaignTypes | Customer | Marketing Campaign Types |
| SLCarrierShip | Customer | Carrier Shipments Table for UPS/FedEx Integration |
| SLCertifications | Employee | Certifications/Licenses |
| SLCfgAttrAlls | Config | Configuration Attributes All Table |
| SLCfgAttrs | Config | Configuration Attributes |
| SLCfgCompAlls | Config | Configuration Components All Table |
| SLCfgComps | Config | Configuration Components |
| SLCfgCustomGroupFields | Config | List of fields from Item and Work Center tables that can be mapped to Custom Groups and Custom Parts in SC Config Powerpack Manager |
| SLCfgMains | Config | Configuration Header |
| SLCfgRefs | Config | Configuration References |
| SLCfgSchemaAttributeFields | Config | List of fields that can be mapped to Schema Attributes in SC Config Powerpack Manager |
| SLChargebacks | Customer | Chargeback |
| SLChargebackTypes | Customer | Chargeback Type |
| SLChartAlls | Finance | Chart of Accounts All |
| SLChartBps | Finance | Chart of Accounts Budget and Plan |
| SLChartDs | Finance | Chart of Account Allocations |
| SLCharts | Finance | Chart of Accounts and Related Forms/Utilities |
| SLChartTaxInfos | Finance | Chart Tax Info |
| SLChartUnitcd1_Alls | Finance | Unit Code 1 tab on Chart of Accounts - All |
| SLChartUnitcd1s | Finance | Unit Code 1 tab on Chart of Accounts |
| SLChartUnitcd2_Alls | Finance | Unit Code 2 tab on Chart of Accounts - All |
| SLChartUnitcd2s | Finance | Unit Code 2 tab on Chart of Accounts |
| SLChartUnitcd3_Alls | Finance | Unit Code 3 tab on Chart of Accounts - All |
| SLChartUnitcd3s | Finance | Unit Code 3 tab on Chart of Accounts |
| SLChartUnitcd4_Alls | Finance | Unit Code 4 tab on Chart of Accounts - All |
| SLChartUnitcd4s | Finance | Unit Code 4 tab on Chart of Accounts |
| SLCitemhs | Customer | History Customer Order Lines and History Customer Order Blanket Releases |
| SLCoAlls | Customer | Customer Orders All - site_ref and co_num as key |
| SLCoBlns | Customer | Customer Order Blanket Lines |
| SLCohAlls | Customer | History Customer Orders All |
| SLCohBls | Customer | History Customer Order Blanket Lines |
| SLCohs | Customer | History Customer Orders All |
| SLCoitemAlls | Customer | Customer Order Lines and a lot of related forms |
| SLCoitemLogs | Customer | Customer Order Lines Change Log |
| SLCoitems | Customer | Customer Order Lines and a lot of related forms |
| SLCoitemShps | Customer | Order Shipping and related forms |
| SLCommdues | Customer | Commissions Due |
| SLCommodities | Vendor | Commodity Codes |
| SLCommtabs | Customer | Commission Table Maintenance |
| SLCompliancePrograms | Material | Compliance Programs |
| SLConInvHdrs | Customer | Consolidated Invoice Generation and Consolidated Invoices Workbench |
| SLConInvItems | Customer | Consolidated Invoice - Summarized Line Detail Info (used in conjunction with SLConInvLines) - for each con_inv_line table record there will be one or more con_inv_item table records. |
| SLConInvLines | Customer | Consolidated Invoice - Summarized Line Info |
| SLContactAlls | Customer | Conctact Details for all sites |
| SLContactgroupContacts | Customer | Sub Collection for SLContactgroups |
| SLContactgroups | Customer | Primary IDO for Sales Contact Group |
| SLContacts | Customer | Contact Details |
| SLContainerItems | Material | Container Item |
| SLContainers | Material | Container |
| SLContention | APS | Contention |
| SLContentionDetails | APS | Contention Details |
| SLCoPackingSlips | Customer | Pre-Ship Packing Selection |
| SLCoparmAlls | Customer | Order Entry Parameters |
| SLCoparms | Customer | Order Entry Parameters |
| SLCos | Customer | Customer Orders and a lot of related forms |
| SLCoShipApprovalLogs | Customer | Co Ship Approval Logs |
| SLCoShips | Customer | Order Shipments and History Order Shipments |
| SLCoSlsComms | Customer | Sales Commission Distribution and related forms |
| SLCostCodes | Codes | Project Cost Codes |
| SLCostingAltCompareCostingAltItems | Material | Costing Alternative Compare Costing Alt Items |
| SLCostingAltCompareItems | Material | Costing Alternative Compare Items |
| SLCostingAltCompareItemWhses | Material | Costing Alternative Compare Item Whses |
| SLCostingAltDepts | Material | Costing Alternative Departments |
| SLCostingAltItems | Material | Costing Alternative Items |
| SLCostingAltMaterials | Material | Costing Alternative Materials |
| SLCostingAltProductCodes | Material | Costing Alternative Product Codes |
| SLCostingAlts | Material | Costing Alternative |
| SLCostingAltWcs | Material | Costing Alternative Wcs |
| SLCountries | Codes | Countries |
| SLCourses | Employee | Training Courses |
| SLCtps | APS | Contains methods used by the CTP process |
| SLCurrates | Codes | Currency Rates |
| SLCurrencies | Adapters | Currency Integration Adapter (XML document interface) |
| SLCurrencyAlls | Vendor | Currency Codes - All |
| SLCurrencyCodeAlls | Codes | Multi Site Currency Codes |
| SLCurrencyCodes | Codes | Currency Codes |
| SLCurrParms | Codes | Currency Parameters |
| SLCurrUks | Codes | Excise Currency Rates |
| SLCustAddrs | Customer | Access custaddr table info in some A/R and Customer forms |
| SLCustdrfts | Finance | A/R Draft-related Forms |
| SLCustLcrs | Customer | Customer Letters of Credit |
| SLCustomerAlls | Customer | Customers All |
| SLCustomerContacts | Customer | Customer Contacts |
| SLCustomerCurrency | Customer | Customer Currency Code |
| SLCustomerPortalCoitems | Customer | IDO used only by the Customer Portal |
| SLCustomerPortalItems | Material | IDO used only by the customer portal |
| SLCustomers | Customer | Customers |
| SLCustomerStatuses | Customer | Customer Statuses |
| SLCustomerSurchargeRules | Customer | Customer Surcharge Rules |
| SLCustomerUsernames | Customer | Customer Usernames |
| SLCustTps | Customer | EDI Customer Profiles |
| SLCusttypes | Codes | Customer Types |
| SLCycles | Material | Cycle Count Posting & Update |
| SLDbMaintParms | Admin | Database Maintenance Parameters |
| SLDccos | DataCollection | Customer Order Shipping Error Processing |
| SLDccoSerials | DataCollection | Customer Order Shipping Error Processing - Serial Numbers tab |
| SLDcitems | DataCollection | Cycle Counting Error Processing |
| SLDcitemSerials | DataCollection | Cycle Counting Error Processing - Serial Numbers tab |
| SLDcjits | DataCollection | Just-in-Time Production Error Processing |
| SLDcjitSerials | DataCollection | Just-in-Time Production Error Processing - Serial Numbers tab |
| SLDcjms | DataCollection | Job Material Transactions Error Processing |
| SLDcjmSerials | DataCollection | Job Material Transactions Error Processing - Serial Numbers tab |
| SLDcmoves | DataCollection | Quantity Move Error Processing |
| SLDcmoveSerials | DataCollection | Quantity Move Error Processing - Serial Numbers tab |
| SLDcparms | DataCollection | Data Collection parameters |
| SLDcphyinvs | DataCollection | Used for Physical Inventory Error Processing |
| SLDcpos | DataCollection | Purchase Order Receiving Error Processing |
| SLDcpoSerials | DataCollection | Purchase Order Receiving Error Processing - Serial Numbers tab |
| SLDcpss | DataCollection | Production Schedule Complete Error Processing |
| SLDcpsSerials | DataCollection | Production Schedule Complete Error Processing - Serial Numbers tab |
| SLDcsfcItems | DataCollection | Job Error Processing - item info |
| SLDcsfcs | DataCollection | Data Collection; Work Center Machine/Labor Time Error Processing |
| SLDcsfcSerials | DataCollection | Job Error Processing - Serial Numbers tab |
| SLDctas | DataCollection | Data collection time and attendance |
| SLDctrans | DataCollection | Transfer Order Receive Error Processing |
| SLDctranSerials | DataCollection | Transfer Order Receive Error Processing - Serial Numbers tab |
| SLDcwcs | DataCollection | Work Center Material Error Processing |
| SLDcwcSerials | DataCollection | Work Center Material Error Processing - Serial Numbers tab |
| SLDelTermAlls | Codes | Delivery Terms All |
| SLDelTerms | Codes | Delivery Terms |
| SLDemandSummaries | APS | Demand Summary MRP-APS |
| SLDepDtlss | Employee | Magnetic Media Direct Deposit |
| SLDepts | Employee | Departments |
| SLDeptSupvs | Employee | Department Supervisors |
| SLDimAttributes | Codes | Dimension Attributes |
| SLDimensionObjects | Codes | Dimension Objects |
| SLDimensions | Codes | Dimensions |
| SLDimFunctions | Codes | Dimension Functions |
| SLDimObjectAttributeInlineList | Codes | Dimension Object Attributes Inline List |
| SLDimObjectAttributes | Codes | Dimension Object Attributes |
| SLDimObjectTableJoins | Codes | Dimension Object Table Joins |
| SLDimSubscribers | Codes | Dimension Subscribers |
| SLDiscounts | Customer | Discounts by Customer Type and Product Code |
| SLDispcodes | Customer | Disposition Codes |
| SLDistAcctAlls | Codes | Distribution Accounts |
| SLDistAccts | Codes | Distribution Accounts |
| SLDivMgrs | Employee | Divisions |
| SLDocProfileCustomers | Customer | Customer Doc Profiles |
| SLDocProfileEmailTemplates | Admin | Document Profile Email Templates |
| SLDocProfileMaterial | Material | Pro Forma Invoice Report |
| SLDocProfileVendors | Vendor | Vendor Document Profile and PO Reports |
| SLDocumentObjectAndRefExtViews | Admin | Document Object Reference Extended View |
| SLDocumentObjectGroupViews | Admin | Document Object Group View |
| SLDocumentObjects_Exts | Admin | Document Object Extended |
| SLDocumentTypeGroups | Admin | Document Type Groups |
| SLDoHdrs | Customer | Delivery Order Header Information |
| SLDoLines | Customer | Delivery Order Line Information |
| SLDoSeqs | Customer | Delivery Order Line Sequences |
| SLDown000s | APS | Used by the Resource Gantt Chart form. Bound to DOWN000, an APS Scheduler output table used to record periods of resource unavailability |
| SLDownplan000s | APS | Bound to DOWNPLAN000, an APS Scheduler output table used to record periods of resource unavailability |
| SLDraftTypes | Finance | Draft Types Form |
| SLDropshiptos | Customer | Drop Ship To Query |
| SLEcndists | Material | ECN Distribution Codes |
| SLEcnhitems | Material | History Engineering Change Notice Items |
| SLecnhs | Material | History Engineering Change Notices |
| SLEcnitems | Material | Engineering Change Notice Items |
| SLEcnpris | Material | ECN Priority Codes |
| SLEcns | Material | Engineering Change Notices |
| SLEdiBols | Customer | EDI Advance Ship Notices |
| SLEdiCoblns | Customer | EDI Customer Order Blanket Lines |
| SLEdiCoitems | Customer | EDI Customer Order Blanket Lines and Releases |
| SLEdiCos | Customer | EDI Customer Orders |
| SLEdiInvHdrs | Customer | EDI Invoice Register Header |
| SLEdiParms | Customer | Demand EDI Parameters |
| SLEdiPoAckBlns | Vendor | EDI Purchase Order Acknowledgement Blanket Lines/Releases |
| SLEdiPoAckItems | Vendor | EDI Purchase Order Acknowledgement Lines |
| SLEdiPoAcks | Vendor | EDI Purchase Order Acknowledgements |
| SLEdiPoitems | Vendor | Collection of outbound EDI Purchase Order Line Items |
| SLEdiPos | Vendor | Retransmit EDI POs and Ship Schedules |
| SLEdiScheds | Vendor | Retransmit EDI Planning Schedules |
| SLEdiVinvs | Vendor | Collection of inbound EDI Vendor Invoice Headers. Runs purge process on Purge EDI Vendor Invoices |
| SLEdiVsnLotSerials | Material | Collection of Lot/Serial number records for inbound EDI Vendor Shipments |
| SLEdMajors | Employee | Education Majors |
| SLEEOClss | Employee | EEO Class |
| SLElectronicSignatures | Admin | Electronic Signatures |
| SLEmpAbsences | Employee | Attendance |
| SLEmpawards | Employee | Employee Awards |
| SLEmpCategories | Employee | Employee Categories |
| SLEmpCerts | Employee | Applicant or Employee Certification/License |
| SLEmpChilds | Employee | Children |
| SLEmpConts | Employee | Emergency Contacts |
| SLEmpEds | Employee | Employee Education |
| SLEmpexams | Employee | Applicant or Employee Exams |
| SLEmpHpos | Employee | Employee Position History |
| SLEmpI9s | Employee | Employment Eligibility |
| SLEmpInjuries | Employee | Employee Injuries |
| SLEmpInss | Employee | Employee Insurance |
| SLEmpinssDependents | Employee | Employee Insurance Dependents |
| SLEmployees | Employee | Employees |
| SLEmployeesInternal | Employee | Internal methods of employees IDO. Not part of any license or permission group. |
| SLEmpMemos | Employee | Employee Memos |
| SLEmpPoss | Employee | Employee Positions |
| SLEmpPrBanks | Employee | Employee - Direct deposit |
| SLEmpProps | Employee | Employee Properties |
| SLEmpRas | Employee | Employee Reimbursement Plans |
| SLEmpreviews | Employee | Employee Performance Reviews |
| SLEmpSalaries | Employee | Employee Salaries |
| SLEmpSelfServPreqitems | Employee | Created for the Employee Self Service Module |
| SLEmpSelfServPreqs | Employee | Created for the Employee Self SErvice Module |
| SLEmpSelfServPrtrxps | Employee | Used by Employee Self Service module |
| SLEmpSelfServPTOAccruedTakenBal | Employee | Created for Employee Self Service Module |
| SLEmpSelfServTimeOffCalendar | Employee | Created for the Employee Self Service Module |
| SLEmpskills | Employee | Employee Skills |
| SLEmpStats | Employee | Employee Status |
| SLEmpSteps | Employee | Applicant or Employee Processing |
| SLEmpWrkExps | Employee | Employee Work Experience |
| SLEndTypeAlls | Customer | End Type All |
| SLEndtypes | Customer | End User Types |
| SLEngineeringNPDCodes | Material | Engineering NPD Codes |
| SLEsigAuthorizations | Admin | SLEsigAuthorization |
| SLEsigTypes | Codes | SLEsigType |
| SLEthnicIds | Employee | Ethnic Id |
| SLEvalcodes | Codes | Evaluation Codes |
| SLEventMessages | Admin | IDO for the Portal Administrator Home |
| SLEventStates | Admin | IDO used for Portal Administrator Home |
| SLExams | Employee |  |
| SLExperiences | Employee | Work Experience |
| SLExportApTrxds | ExtFin | External Financial Interface - Export A/P Transaction Details |
| SLExportApTrxs | ExtFin | External Financial Interface - Export A/P Transactions |
| SLExportArInvds | ExtFin | External Financial Interface - Export A/R Transaction Details |
| SLExportArInvs | ExtFin | External Financial Interface - Export A/R Transactions |
| SLExportArTermsDues | ExtFin | AR terms Due records when an invoice has multiple due dates |
| SLExtfinParms | ExtFin | External Financial Interface Parameters |
| SLExtPRInterfaceErrors | Admin | External Payroll Interface |
| SLExtPRInterfaces | Admin | External Payroll Interface |
| SLFabonuses | Codes | Bonus Depreciation Codes |
| SLFaclasses | Codes | Fixed Asset Class Codes |
| SLFaCosts | Finance | Fixed Asset Costs |
| SLFaDeprs | Finance | Fixed Asset Depreciation |
| SLFadeptabs | Finance | Fixed Asset Depreciation Tables |
| SLFaDisps | Finance | Fixed Asset Disposal |
| SLFaDists | Finance | Fixed Asset Disposal Distributions |
| SLFamasters | Finance | Fixed Assets |
| SLFamCodes | Material | Family Codes |
| SLFaparms | Finance | Fixed Asset Parameters |
| SLFaTrans | Finance | Fixed Asset Transfer |
| SLFavoriteCustomers | Customer | My Favorite Customer |
| SLFeatItems | Material | Feature Group Ranks |
| SLFeatqties | Customer | Customer Orders - Feature Groups info |
| SLFeatranks | Material | Feature Group Re-ranks |
| SLFeatures | Material | Feature Groups |
| SLFinanceHubAP | Finance | IDO for Finance hub AP |
| SLFinanceHubAR | Finance | IDO for Finance hub AR |
| SLFingroups | Finance | Financial Statement Groups |
| SLFinTargetGroupAccounts | Finance | Target Group Accounts |
| SLFinTargetGroupActualDetails | Finance | Target Group Actual Details |
| SLFinTargetGroupHistoricalRun | Finance | Fin Target Group Historical Run |
| SLFinTargetGroups | Finance | Target Groups |
| SLFinTargetGroupTypes | Finance | Target Group Types |
| SLFiscalRptSystems | Finance | Fiscal Reporting Systems |
| SLFiscalRptSystemTypes | Finance | Fiscal Reporting System Types |
| SLFixedAssetMovementDetailReport | Report | Fixed Asset Movement Detail Report |
| SLFixedAssetMovementReport | Report | Fixed Asset Movement Report |
| SLForecasts | Material | Forecast |
| SLFormActionThresholds | Admin | Form Action Thresholds |
| SLFormAdoption | Admin | Form Adoption |
| SLForms | Config | Forms used to select Configuration Parts and Attribute Values |
| SLFsbJournals | Finance | FsbJournals |
| SLFsbPeriods | Finance | Multi-FSB Accounting Periods |
| SLFsbs | Finance | Financial Set of Books |
| SLGantt | APS | Contains method used by Gantt charts |
| SLGDPdUMedia | DELOC | Media Set for GDPdU Reports |
| SLGenAPTrans | Vendor | Supports form Generate A/P Transactions |
| SLGenAPTransFilterString | Vendor | Supports form Generate A/P Transactions |
| SLGeneralLedgerTransactionS01DNReport | Report | General Ledger Transaction S01DN Report |
| SLGeneralLedgerTransactionS03aDNReport | Report | General Ledger Transaction S03aDN Report |
| SLGlbanks | Finance | Bank Transaction Information for Reconciliation and Voiding Posted Payments |
| SLGlrpthcs | Finance | Financial Statement Definition Columns |
| SLGlrpths | Finance | Financial Statement Definition and Preview |
| SLGlrptlAlls | Finance | Financial Statements |
| SLGlrptlcs | Finance | Financial Statement Line Definition |
| SLGlrptls | Finance | Financial Statement Preview - grid |
| SLGlrptlss | Finance | Financial Statement Line Definition - grid on Total tab |
| SLGLVoucherReport | Report | oGLVoucherReport |
| SLGNTHLCATs | APS | Used by the Resource Gantt Chart. Tied to GNTHLCAT table (catalog of user-defined highlights - names only) |
| SLGNTHLCRITs | APS | Used by the Resource Gantt Chart. Tied to GNTHLCRIT table (contains one or more criteria that define each highlight) |
| SLGNTPREFSs | APS | Used by the Resource Gantt Chart. Tied to GNTPREFS table (Gantt User Preferences) |
| SLGNTSELCATs | APS | Used by the Resource Gantt Chart. Tied to GNTSELCAT table (catalog of user-defined resource selections -  group of resources selected for viewing in Gantt chart) |
| SLGNTSELMBRs | APS | Used by the Resource Gantt Chart. Tied to GNTSELMBR (contains the names of the resources for each resource selection) |
| SLGoBDUMedia | DELOC | Media Set for GoBDU Reports |
| SLGrnHdrs | Vendor | Goods Receiving Notes and Related Forms |
| SLGrnLines | Vendor | Goods Receiving Notes Lines |
| SLHighKeys | MGCore | View of NextKeys table without duplicates or non-high values |
| SLHorizons | Codes | Planning Horizon Calendar |
| SLHrparms | Employee | Human Resources Parameters |
| SLHrSteps | Employee | Processing Steps |
| SLI9docs | Employee | I-9 Documents |
| SLIncoDelTerms | Codes | INCOTERM 2000 codes |
| SLIndcodes | Product | Indirect Labor Codes |
| SLInsAges | Employee | Insurance - Price per 1000 tab |
| SLInsHcs | Employee | Insurance - Coverage Classes |
| SLInsurances | Employee | Insurance |
| SLInteractionTopics | Customer | Interaction Topics |
| SLIntranets | MGCore | Intranets |
| SLIntraSiteTransferDetails | Material | SLIntraSiteTransferDetails |
| SLIntraSiteTransferSupDems | Material | SLIntraSiteTransferSupDems |
| SLIntraSiteTransferWhses | Material | Distribution Warehouses |
| SLInvBatchDetails | Customer | Invoice Batch Details |
| SLInvBatchs | Customer | Invoice Batchs |
| SLInvCategories | Customer | It's a collection of Invoice categories from inv_category table( Used in Invoice Categories, Void Unused Invoices, Invoice / Credit Memo / Debit Memo Sequences Forms) |
| SLInvcLangs | Customer | Multi-Lingual Order Invoice |
| SLInventoryLevels | APS | Inventory Level form |
| SLInventorySummaries | APS | Inventory Summary form |
| SLInvHdrAlls | Customer | Order Invoicing Credit Memo and RMA Cred |
| SLInvHdrs | Customer | Order Invoicing Credit Memo and RMA Credit Memo |
| SLInvItemAlls | Customer | Invoice Listing |
| SLInvMs | Projects | Invoice Milestones and Related Forms |
| SLInvMsLogs | Projects | Audit Tab on Invoice Milestones and Related Forms |
| SLInvMsSeqs | Projects | Requirements Tab on Invoice Milestones and Related Forms |
| SLInvoiceBuilders | Customer | Used for Invoice Builder Form |
| SLInvparms | Material | Inventory Parameters and Transfer Order Parameters |
| SLInvplan000s | APS | Bound to INVPLAN000, an APS Scheduler output table used to record supply and demand that affects material inventory |
| SLInvSequences | Customer | Its the collection that is used in the Invoices /Credit/ Debit Memo Sequences form. It uses the inv_sequences table along with the inv_category table to take the description of the category. |
| SLInvVoids | Customer | It will be used for Voiding Invoice Numbers,Base Table for this IDO is inv_void. ( Used in Voided Invoices , Void Unused Invoices Forms) |
| SLISOBankTranDomainFamilies | Codes | ISO Bank Transaction Domain Family Codes |
| SLISOBankTranDomains | Codes | ISO Bank Transaction Domain Codes |
| SLISOBankTranDomainSubFamilies | Codes | ISO Bank Transaction Domain Sub Family |
| SLISOCountries | Codes | ISO Countires |
| SLISOCurrencyCodes | Codes | ISO Currency Codes |
| SLISOUMs | Codes | ISO Unit of Measure Codes |
| SLItemacts | Material | Miscellaneous Issue, Quantity Adjustment, or Manual LIFO/FIFO Adjustment |
| SLItemAlls | Material | Items All |
| SLItemCategories | Material | IDO for Item Catagories |
| SLItemCategoryItems | Material | IDO for Item Category Items |
| SLItemCategoryLangs | Material | IDO for Item Catatory Language |
| SLItemContentExchanges | Codes | Item Content Exchanges |
| SLItemContentPrices | Codes | Item Content Prices |
| SLItemContentRefs | Customer | Item Content References |
| SLItemContents | Codes | Item Contents |
| SLItemCustPriceAlls | Customer | Customer Item Cross Reference Prices |
| SLItemCustPrices | Customer | Customer Item Cross Reference Prices |
| SLItemcusts | Customer | Customer Item Cross References |
| SLItemGlbls | Material | Global Items |
| SLItemLangs | Material | Multi-Lingual Item |
| SLItemLifos | Material | Item Lifo Fifo Stack |
| SLItemlocAlls | Material | Item Stockroom Locations All |
| SLItemLocs | Material | Item Stockroom Locations and Related Utilities |
| SLItemprices | Material | Item Pricing or Change Item Price |
| SLItemrevs | Material | Delete Item Revision |
| SLItems | Material | Item master |
| SLItemsNonInventoryItems | Material | Listed Items and Non-Inventory Items |
| SLItemVendPriceAlls | Vendor | Item Vendor Cross Reference Prices |
| SLItemVendPrices | Vendor | Item Vendor Cross Reference Prices |
| SLItemvends | Vendor | Item/Vendor Cross References |
| SLItemwhses | Material | Item Warehouses, Item Initialization, and Set YTD/PTD to Zero |
| SLJobacts | Product | Jobacts IDO |
| SLJobAlls | Product | Job Orders for All Site Group |
| SLJobCoitems | Product | Estimation Worksheet |
| SLJobitems | Product | Co-Product Job Orders |
| SLJobMatlAlls | Product | Job Materials for All Site Group |
| SLJobmatlCompliances | Product | Job Materials Compliances |
| SLJobmatlJobs | Product | Job Materials - Cross References to Jobs |
| SLJobmatlPos | Product | Jobmatl cross references to purchase orders (where used) |
| SLJobmatlReqs | Product | Job Materials - Cross References to Requisitions |
| SLJobmatls | Product | Jobmatl IDO |
| SLJobmatlTrns | Product | Job Materials - Cross References to Transfer Orders |
| SLJobplan000s | APS | Bound to JOBPLAN000, an APS Scheduler output table used to record information about each operation in the plan |
| SLJobPriceBreaks | Product | Job Price Break |
| SLJobQueues | MGCore | Job Queue Information |
| SLJobRefs | Product | Job Material References |
| SLJobRouteAlls | Product | Jobroute IDO for All Sites |
| SLJobRoutes | Product | Jobroute IDO |
| SLJobs | Product | Job Orders and related forms |
| SLJobSchs | Product | Job Schedule |
| SLJobtCls | Product | Pending Job Labor Transactions |
| SLJobtMats | Product | Pending Material Transactions |
| SLJobTranAlls | Product | Job Transaction for All Site Group |
| SLJobtranitems | Product | Unposted Job Transactions - Co-products Grid |
| SLJobTrans | Product | Job Transaction-related Forms |
| SLJobtSers | Product | Pending Serial Transactions |
| SLJourHdrs | Admin | Jounal Header Information |
| SLJournalCompressReport | Report | Journal Compress Report |
| SLJournalControlNumberReport | Report | Journal Control Number Report |
| SLJournals | Finance | Journals |
| SLJournalTransactionReport | Report | oJournalTransactionReport |
| SLJrtItems | Product | Job Operations - Co-products tab |
| SLJrtResourceGroups | Product | Resource grid on Job Operations and Related Forms |
| SLJrtSchs | Product | Jobroute Schedule records |
| SLJsattr000s | Product | Bound to JSATTR, an APS input table that contains operation attribute values |
| SLLateJobs | APS | Late Jobs |
| SLLcRcpts | Vendor | Generate Landed Cost Vouchers |
| SLLeadAlls | Customer | Leads |
| SLLeads | Customer | Leads |
| SLLeadStatuses | Customer | Lead Statuses |
| SLLedgerAlls | Finance | G/L Posted Transactions |
| SLLedgers | Finance | G/L Posted Transactions |
| SLLocationAlls | Material | Locations All |
| SLLocations | Material | Locations |
| SLLockableFunctions | Admin | Unlock Locked Functions |
| SLLOOKUP000s | APS | Setup Matrix |
| SLLookuphdrs | APS | Used by the Setup Matrix form. Bound to LOOKUP000, an APS Scheduler table used for looking up a value based on two parameters |
| SLLotAlls | Material | Lots All |
| SLLotLocAlls | Material | Item Lot Locations All |
| SLLotLocs | Material | Item Lot Locations |
| SLLots | Material | Lots and Delete Lots |
| SLMachineDowntimeCodes | Codes | Machine Downtime Codes |
| SLMachineSetupTimeVariance | Product | Machine Setup Time |
| SLManufacturerItems | Material | Manufacturer Items |
| SLMasterPlanningReport | Report | Master Planning Report |
| SLMaterialListing | Product | Routing BOM Listing - Grid |
| SLMATLALTnnns | APS | Planner ALTernate MATL ID cross reference |
| SLMATLATTRnnns | APS | Planner ATTribute ID corss reference |
| SLMATLnnns | APS | Planner Items - MATERIAL ID |
| SLMATLPBOMSnnns | APS | Planner BOM ID Cross reference |
| SLMatlplan000s | APS | Bound to MATLPLAN000, an APS Scheduler output table that summarizes schedule event records |
| SLMATLPPSnnns | APS | Planner PROCedure PLAN ID cross reference |
| SLMatltranAlls | Material | Posted Transaction and Delete Material Transactions |
| SLMatltranAmts | Material | Posted Transaction - Grid |
| SLMatltrans | Material | Posted Transaction and Delete Material Transactions |
| SLMemoTopics | Employee | Memo Topics |
| SLMilitaries | Employee | Military Service |
| SLMobileDeleteTrackings | Mobile | Delete Tracking for mobile updates |
| SLMobileDeviceChildIDOs | Mobile | Child IDOs on mobile device |
| SLMobileDeviceDatas | Mobile | Mobile Device Synchronization Data |
| SLMobileDeviceFields | Mobile | Custom Mobile Fields |
| SLMobileDeviceGroups | Mobile | Groups allowed to acess the Mobile Ext. |
| SLMobileDeviceIDOFilters | Mobile | Row Filters for Mobile IDOs |
| SLMobileDeviceIDOLinks | Mobile | Parent/Child IDO Link on Mobile |
| SLMobileDeviceIDOs | Mobile | IDO Collections to use on mobile |
| SLMobileDeviceUsers | Mobile | Users allowed to access the Mobile Ext. |
| SLMobileParms | Mobile | Mobile Parameters |
| SLMrpExcs | Product | Exception Message Priorities |
| SLMrpParms | Product | Planning Parameters |
| SLMrpWbs | Material | Material Planner Workbench and Related Utilities |
| SLMsgBwsrs | Admin | Message Query |
| SLMSMoves | Material | Multi-Site Quantity Move |
| SLMSSerials | Material | Multi-Site Quantity Move - Serial Numbers tab grid |
| SLMXCFDIReport | Report | Mexico CFDI Report |
| SLNonInventoryItems | Material | Non Inventory Items |
| SLNonTrans | NonTrans | IDO for methods that can't run in the context of a transaction, but have not yet been moved to a better place (obsolescent) |
| SLObjectMainMessages | Admin | Message Query |
| SLObjectNotes | Codes | Notes - primary data source |
| SLOffices | Employee | Offices |
| SLOPMMethods | Customer | OPMMethods |
| SLOpportunities | Customer | Opportunities |
| SLOpportunityAlls | Customer | Opportunities |
| SLOpportunityMembers | Customer | Opportunity Members |
| SLOpportunitySources | Customer | Opportunity Sources |
| SLOpportunityStages | Customer | Opportunity Stages |
| SLOpportunityStatuses | Customer | Opportunity Status |
| SLOpportunityTaskAlls | Customer | Opportunity Tasks |
| SLOpportunityTasks | Customer | Opportunity Tasks |
| SLOpportunityTaskTypes | Customer | Opportunity Task Types |
| SLOptionalModules | Admin | ooptionalmodules |
| SLOrderStatuses | Adapters | Order Status Integration Adapter (XML document interface) |
| SLOrdplan000s | APS | Bound to ORDPLAN000, an APS Scheduler output table used to record projected dates for planned orders |
| SLOrgCpnys | Employee | Companies |
| SLPackWorkbenchs | Customer | Pack Workbench |
| SLParms | Codes | General Parameters |
| SLParmsAlls | Vendor | General Parameters - All |
| SLPartySyncs | Adapters | Party Synchronization Integration Adapter (XML document interface) |
| SLPBOMMATLSnnns | APS | Planner BOM Materials |
| SLPBOMnnns | APS | Planner BOM |
| SLPckHdrs | Customer | Packing Slip info (used in utilities) |
| SLPckitems | Customer | Used for Packing Slip on Invoice |
| SLPeggingDisplays | Material | Pegging Display |
| SLPeriods | Finance | Accounting Periods |
| SLPeriodsSeqs | Finance | Accounting Period Control Number Sequences |
| SLPerSorts | Finance | Period Sorting Methods |
| SLPertots | Finance | Handles per-tot table data for several utilities |
| SLPhyinvs | Material | Used for Physical Inventory Error Processing |
| SLPhytags | Material | Set Tag Sheet Controls |
| SLPickLists | Customer | Pick Lists |
| SLPickMachByWcs | Product | Allows the Machine browser to only show Machine Resource IDs associated with the entered Work Centers that have been released to the Production Floor |
| SLPickWorkbenchs | Customer | Pick Workbench |
| SLPitemhs | Vendor | History Purchase Order Lines and History PO Blanket Line/Releases |
| SLPItems | Product | Production Schedule Items |
| SLPkgLabelTemplates | Customer | Package Label Templates |
| SLPlanint000s | Product | Resource Planning Intervals |
| SLPlanningDetails | Material | Planning Detail and Related Forms |
| SLPlanRas | Employee | Reimbursement Plan |
| SLPlants | Material | Plants |
| SLPLARAPReportsforaDay | Report | AR AP Report for a Day Accounts |
| SLPLARAPSettlementAsOfDayReport | Report | Poland AR-AP Settlement As of Day Report |
| SLPLInventoryAsOfDayReport | Report |  |
| SLPLInventoryForADayReport | Report |  |
| SLPLInvKSeFMarkingAlls | PLLOC | Invoice KSeF Marking Alls |
| SLPLInvKSeFMarkings | PLLOC | Poland Invoice KSeF Markings |
| SLPLKSeFCertificates | PLLOC | Poland KSeF Certificates |
| SLPLKSeFLogs | PLLOC | KSeF API Logs |
| SLPLKSeFMarkings | PLLOC | Marking ID for Poland KSeF E-Invoicing |
| SLPLKSeFParms | PLLOC | Parameters for Poland KSeF E-Invoicing |
| SLPLKSeFUsers | PLLOC | User configuration for Poland KSeF E-Invoicing |
| SLPlnSupplySourceRuleDtls | Material | Supply Source Rule Details |
| SLPlnSupplySourceRules | Material | Supply Source Rules |
| SLPlnSupplySrcRuleDtls | Material | Supply Source Rule Details |
| SLPlnSupplySrcRules | Material | Supply Source Rules |
| SLPLOrderProFormaInvoiceReport | Report | Order Pro Forma Invoice Report |
| SLPLPOReceivingSettlementReport | Report | PO Receiving Settlement |
| SLPLProFormaInvHdrs | PLLOC | Pro Forma Invoice Headers |
| SLPLProFormaInvItems | PLLOC | Pro Forma Invoice Lines |
| SLPLProjectWIPAsOfDayReport | Report | Project WIP As Of Day Report |
| SLPLProjectWIPForADayReport | Report | Project WIP For A Day Report |
| SLPLStaxAccepts | PLLOC | Poland Tax Acceptance IDO |
| SLPLTurnoverBalances | PLLOC | Turnover and Balances |
| SLPLTurnoverBalancesReport | Report | Turnover and Balances Report |
| SLPLVATWhiteListParms | PLLOC | Parameters and methods for verifying the status of VAT/VIES/GUS taxpayers |
| SLPLVendorWhiteListCheckLog | PLLOC | PL Vendor White List Check Logs |
| SLPoAlls | Vendor | Purchase Orders All |
| SLPoBlnhs | Vendor | History PO Blanket Lines |
| SLPoBlns | Vendor | Purchase Order Blanket Lines |
| SLPochanges | Vendor | PO Change Orders |
| SLPohs | Vendor |  |
| SLPoItemAlls | Vendor | PO Blanket Releases and Related Forms - All |
| SLPoitemLogs | Vendor | Purchase Order Lines Change Log |
| SLPoItems | Vendor | PO Blanket Releases and Related Forms |
| SLPoItmchgs | Vendor | PO Change Orders - Grid |
| SLPoLangs | Vendor | Purchase Order Language Translations |
| SLPOMissingInformationViews | Vendor | Purchase Orders Missing Information |
| SLPoparms | Vendor | Purchasing Parameters |
| SLPoRcpts | Vendor | Purchase Order Receipts or History PO Receipts |
| SLPortalCompanyProfile | Customer | Created for Customer Portal My Compny Profile web page |
| SLPortalCompanyShipTos | Customer | Created for Customer Portal My Compny Profile web page |
| SLPortalFSUnits | FSPlusUnit | IDO created for SyteLine Portals |
| SLPortalInventory | Material | Created for the CP Inventory web page |
| SLPortalProducts_H_Views | Material | Portal Products View |
| SLPortalProducts_HC_Views | Material | Portal Products View |
| SLPortalProducts_HCD_Views | Material | Portal Products View |
| SLPortalProducts_HCDI_Views | Material | Portal Products View |
| SLPortalProducts_HCI_Views | Material | Portal Products View |
| SLPortalProducts_HD_Views | Material | Portal Products View |
| SLPortalProducts_HDI_Views | Material | Portal Products View |
| SLPortalProducts_HI_Views | Material | Portal Products View |
| SLPortalProductsViews | Material | Portal Products View |
| SLPortalsDocumentObjectGroupViews | Admin | Document Object Group View |
| SLPos | Vendor | Purchase Orders and a lot of related forms |
| SLPosChgs | Employee | Position Change Reasons |
| SLPosClasss | Employee | Position Classifications |
| SLPosDets | Employee | Positions - grid |
| SLPositions | Employee | Positions - grid |
| SLPositivePayFormatFields | Finance | Positive Pay Format Fields |
| SLPositivePayFormatSections | Finance | Positive Pay Format Section |
| SLPosRqmts | Employee | Position Requiremenst |
| SLPostedARTermsDues | Customer | ARPostedInvoiceDueDates - update the date on invoices with multiple due dates |
| SLPostedInvs | Customer | Posted Invoices |
| SLPrbanks | Employee | Direct Deposit Banks |
| SLPrdecds | Employee | Deduction and Earning Codes |
| SLPreqcodes | Vendor | Purchase Order Requisition Codes |
| SLPreqitems | Vendor | Purchase Order Requisition Lines |
| SLPreqs | Vendor | Purchase Order Requisitions |
| SLPrHrss | Employee | Payroll Hours |
| SLPriAdjInvs | Customer | Used on the Price Adjustment Invoice forms |
| SLPricecodeAlls | Material | Price Codes All |
| SLPricecodes | Material | Price Codes |
| SLPriceformulas | Customer | Price Formulas |
| SLPricematrixs | Customer | Price Matrix |
| SLPricePromotions | Customer | Promotion Codes for Promotional and Reba |
| SLPriceQuotes | Adapters | Price Quote Integration Adapter (XML document interface) |
| SLPrLogs | Employee | Payroll Log Hours for Pay Period |
| SLProbcodes | Customer | Problem Codes |
| SLPROCPLNnnns | APS | Planner PROCedure PLaN |
| SLProdcodeAlls | Codes | Product Codes - All |
| SLProdcodes | Codes | Product Codes |
| SLProdMixes | Material | Co-Product Mix |
| SLProdMixIrts | Material | Co-Product Mix Operations |
| SLProdMixItems | Material | Co-Product Mix - Grid |
| SLProductCatalogs | Adapters | Product Catalog Integration Adapter (XML document interface) |
| SLProductionHubAP | Product | Production Hub All Production |
| SLProductionPlannerViews | Product | Production Planner Home |
| SLProFormaInvHdrAlls | Customer | Pro Forma Invoice Header Alls |
| SLProFormaInvHdrs | Customer | Pro Forma Invoice Header |
| SLProFormaInvItems | Customer | Pro Forma Invoice Items |
| SLProFormaStaxs | Customer | Pro Forma Invoice Sales Tax |
| SLProgbills | Customer | Progressive Billings - grid |
| SLProjAlls | Projects | Projects All |
| SLProjBolItems | Projects | Project ASNs |
| SLProjBols | Projects | Project Advance Ship Notices |
| SLProjCostAlls | Projects | Project Cost for All Sites |
| SLProjcostdetailAlls | Projects | Project Cost Details for All Sites |
| SLProjCosts | Projects | Project Control Cost Detail by Cost Code |
| SLProjectHub | Projects | Project Hub |
| SLProjectHubRequisitionsSourcing | Projects | Project Hub Requisitions Sourcing |
| SLProjectHubSROsSourcing | Projects | Project Hub SROs Sourcing |
| SLProjectHubTransferSourcingProject | Projects | Project Hub Transfer Sourcing Project |
| SLProjLabrs | Projects | Project Labor Transactions |
| SLProjMatlAlls | Projects | Project Resource for All Sites |
| SLProjMatls | Projects | Project Resources |
| SLProjParms | Projects | Project Parameters |
| SLProjPckHdrs | Projects | Project Packing Slip and Related Forms |
| SLProjs | Projects | Projects |
| SLProjShips | Projects | Project Resources - Shipping Tab |
| SLProjTaskAlls | Projects | Project Tasks for All Site |
| SLProjTasks | Projects | Project Tasks and Related Forms |
| SLProjTranAlls | Projects | Project Transactions for All Sites |
| SLProjtypes | Codes | Project Types |
| SLProjWipAdjViews | Projects | data source for Project Wip Adjustments form |
| SLProjWorkResources | Projects | Project Work Resources eg. User, Employee, Vendor etc... |
| SLProspectAlls | Customer | Prospect |
| SLProspectContacts | Customer | Prospect Contacts |
| SLProspects | Customer | Prospect |
| SLPrparms | Employee | Payroll Parameters |
| SLPrtaxts | Employee | Tax Codes Exempt and W2 State FIPS Number Entry |
| SLPrtrxds | Employee | Payroll Distribution |
| SLPrtrxps | Employee | Delete Payroll Transactions and W2 Mag Media Electronic Filing |
| SLPrtrxs | Employee | Payroll Processing and Related Utilities |
| SLPs | Product | 2 |
| SLPsitems | Product | Production Schedule Items |
| SLPurchaseOrders | Adapters | Purchase Order / Quote Integration Adapter (XML document interface) |
| SLPurchaseVATRegister012GTGT | Report | Format for Vietnam localization |
| SLPushPassSettings | APS | APS Push Pass Setting |
| SLQualifierStrings | Material | Feature Group Qualifiers |
| SLRbwsPm | Product | RBWS Production Manager Workspace |
| SLRcpts | Material | Master Production Schedule and Related Utilities |
| SLReasons | Codes | Used for various Reason Codes |
| SLRebalanceCustomerBalancesMessageReport | Report | Rebalance Customer Balances Message Rpt |
| SLRefreshData | Admin | IDO for CSI Suite Refresh |
| SLRelatedItems | Material | IDO for Related Items |
| SLReleaseManagement | Admin | Release Management for upgrade |
| SLRepCategories | MGCore | Replication Categories |
| SLReplicationTriggers | MGCore | Code to generate replication triggers. |
| SLRepObjectCategories | MGCore | Replication Categories - grid |
| SLReports | Customer | Used to get current year or report labels in some reports |
| SLRepRules | MGCore | Replication rules |
| SLResattr000s | Product | Bound to RESATTR, an APS input table that contains resource attribute values |
| SLResGrps | Product | Where Used Resource Groups |
| SLResourceGroupDispatchListReport | Report | Resource Group Dispatch List Report |
| SLResourceGroupUtilizations | APS | Resource Group Utilization |
| SLResourcePlans | APS | Resource Plan |
| SLResourceSchedSortCols | Product | Resource Schedules Sort Columns |
| SLResourceTypes | Product | Resource Type |
| SLResourceUtilizations | APS | Resource Utilization MRP-APS |
| SLResrc000s | Product | Resources |
| SLResRefs | Product | Where Used Resources |
| SLResschd000s | Product | Resource Sequencing Or Resource Group Sequencing |
| SLRetentions | Codes | Project Retention Codes |
| SLRetScheds | Codes | Project Retention Codes - grid |
| SLReviews | Employee | Review Types |
| SLRevMs | Projects | Revenue Milestones and Related Forms |
| SLRevMsLogs | Projects | Audit Tab on Revenue Milestones and Related Forms |
| SLRevMsSeqs | Projects | Requirements Tab on Revenue Milestones and Related Forms |
| SLRgattr000s | Product | Bound to RGATTR, an APS input table that contains resource group attribute values |
| SLRGBottleneckDetails | APS | Resource Group Bottleneck Details |
| SLRGBottlenecks | APS | Resource Group Bottlenecks |
| SLRgrp000s | Product | Resource Groups |
| SLRgrpItems | Product | Where Used Resource Groups - Items |
| SLRgrpJobs | Product | Where Used Resource Groups - Jobs |
| SLRgrpmbr000s | Product | Resource Groups - Resources tab |
| SLRgrpRefs | Product | Where Used Resource Groups |
| SLRgrpWcs | Product | Where Used Resource Groups - Work Centers |
| SLRmaitemAlls | Customer | RMA Line Items |
| SLRmaitems | Customer | RMA Line Items |
| SLRmaitmLogs | Customer | Delete RMA Item Log Entries |
| SLRmaparms | Customer | RMA Parameters |
| SLRmarepls | Customer | RMA Line Items - Replacement Lines |
| SLRmas | Customer | RMAs |
| SLRptOpts | MGCore | Report Options Table |
| SLRptOptValues | MGCore | Report Option Values by userid |
| SLRsvdInvAlls | Material | Reservations for Item or Reservations for Order |
| SLRsvdInvs | Material | Reservations for Item or Reservations for Order |
| SLSalChgs | Employee | Salary Change Reasons |
| SLSalesForecastOpportunities | Customer | Primary Collection of Sales Forecast Opportunity |
| SLSalesForecasts | Customer | Primary Collection for Sales Forecast |
| SLSalesPeriods | Customer | Primary Collection for Sales Period |
| SLSalesTeamMembers | Customer | Sales Team Members |
| SLSalesTeams | Customer | Sales Teams |
| SLSalesVATRegister011GTGT | Report | Format for Vietnam Localization |
| SLSchedDemandDetails | APS | Demand Detail - Scheduler |
| SLSchedDemandSummaries | APS | Demand Summary - Scheduler |
| SLSepAttrib | Product | Separation Attributes |
| SLSerialAlls | Material | Serial Numbers, Delete Serials, or Post Job WIP Move Transactions |
| SLSerials | Material | Serial Numbers, Delete Serials, or Post Job WIP Move Transactions |
| SLSetupGroups | Product | Setup Groups |
| SLSfcparms | Product | Shop Floor Control Parameters |
| SLShadowValues | MGCore | Multi-site replication data table. |
| SLShadowValuesErrors | MGCore | Inbound replication errors. |
| SLShift000s | Product | Scheduling Shifts |
| SLShiftexdi000s | Product | Resources - Shift Exceptions Tab |
| SLShifts | Codes | Shift Codes |
| SLShipcodeAlls | Codes | Ship Via Codes All |
| SLShipcodes | Codes | Ship Via Codes |
| SLShipCos | Customer | Shipping Processing Orders |
| SLShipItems | Customer | Shipping Processing Line Releases |
| SLShipLangs | Customer | Multi Lingual Ship Via |
| SLShipmentLines | Customer | Shipment Master Lines |
| SLShipmentPackages | Customer | Shipment Master Packages |
| SLShipmentRefCharges | Customer | Shipment Reference Charges |
| SLShipments | Customer | Shipment Master |
| SLShipmentSeqs | Customer | Shipment Seqs - Package Contents |
| SLShipmentSeqs_FT | Customer | Shipment Seqs - Package Contents |
| SLShipmentSeqSerials | Customer | Shipment Seq Serials - Packaged Serial Numbers |
| SLShipmentSeqUnpacks | Customer | Shipment Unpack Inventory |
| SLShipProcs | Customer | Shipping Processing Batches |
| SLShipTos | Codes | Drop Ship To |
| SLShortageDetails | APS | Shortage Details -  Report |
| SLShortages | APS | Shortages - Report |
| SLSicklves | Employee | Employee Sick Leave |
| SLSiteGroups | MGCore | Site Groups |
| SLSiteGroupsSelection | Codes | SL Site Groups Selection |
| SLSiteLinkInfos | MGCore | Sites/Entities - Link Info tab |
| SLSiteMgmtTableData | Admin | Site Management Table Data |
| SLSitenets | Material | Inter-Site Parameters |
| SLSites | MGCore | Sites/Entities |
| SLSitesSelection | Codes | SL Sites Selection |
| SLSiteUserMaps | MGCore | User ids to use when logging in for replication. |
| SLSkills | Employee | Skills |
| SLSlparms | Employee | Sick Leave Parameters |
| SLSlsclass | Customer | Salesperson Classifications |
| SLSlsmans | Customer | Salespersons |
| SLSSDs | Customer | EC SSDs and Project Resource Shipping SSDs |
| SLStates | Codes | Prov/States |
| SLStockActItems | Material | Miscellaneous Receipt |
| SLSupDems | Material | SLSupDems IDO |
| SLSupEdiParms | Vendor | Supply EDI Parameters - Interface Setup |
| SLSupplyUsageDemands | APS | Supply Usage MRP-APS - demand subcollection |
| SLSupplyUsages | APS | Supply Usage MRP-APS |
| SLSystemTypes | MGCore | System Types |
| SLTaxcodeAlls | Codes | Tax Codes - All |
| SLTaxcodes | Codes | Tax Codes |
| SLTaxFreeExports | Material | Tax Free Exports |
| SLTaxFreeImportItems | Material | Tax Free Import Items |
| SLTaxFreeImports | Material | Tax Free Imports |
| SLTaxItemJurs | Codes | Tax Codes for Items by Jurisdiction |
| SLTaxJurs | Codes | Tax Jurisdiction |
| SLTaxparms | Codes | Tax Parameters |
| SLTaxSystems | Codes | Tax Systems |
| SLTenantDataCleanup | Admin | CSI Tenant Data Cleanup API |
| SLTerminations | Employee | Termination Reasons |
| SLTermLangs | Customer | Multi Lingual Terms |
| SLTerms | Codes | Billing Terms |
| SLTermsAlls | Vendor | IDO on termsl_all table |
| SLTermsSeqs | Codes | Billing Terms - track the sequence of a multiple due date record |
| SLTerritories | Customer | Territories |
| SLTimeatts | DataCollection | Time & Attendance Log |
| SLTmpAckPoBlns | BusInterface | Temp table used for importing PO Acknowledgements |
| SLTmpAckPoitems | BusInterface | Temp table for importing PO Acknowledgements |
| SLTmpAckPos | BusInterface | Temp table used for importing PO Acknowledgements |
| SLTmpCoShips | Customer | Pre-Ship Packing Selection - Shipping tab |
| SLTmpDbMaintCompressions | Admin | used to display generated SQL statements by ProcessCompression method |
| SLTmpExportExtfinBatches | ExtFin | External Financial Interface - Temporary Export External Financial Batches |
| SLTmpExportPoRcpts | BusInterface | Handles the temp table for PO receipt exports |
| SLTmpForecastImport | Material | IDO used for bulk import of forecast data |
| SLTmpGobdMediaDatas | DELOC | Media Data Index for Gobd Reports |
| SLTmpInvoiceBuilders | Customer | Used in Invoice Builder |
| SLTmpJobSplits | Product | Job Lot Splitting |
| SLTmpLCTaxDists | Vendor | Supports the Taxes tab subcollection on the Generate Landed Cost Vouchers form |
| SLTmpMsgBuffers | Material | for using temporary message buffer |
| SLTmpPoBuilders | Vendor | Handles the temp table for PO Builder |
| SLTmpShipSeqs | Customer | Temperary Table for Shipment Seq Records |
| SLTmpShipSeqSerials | Customer | Temperary Table for Shipment Sequence Serials |
| SLTmpVoucherBuilders | Vendor | Handles the temp table for Voucher Builder |
| SLTrainings | Employee | Applicant or Employee Training Courses |
| SLTransferAlls | Material | Transfer Orders and Related Utilities |
| SLTransfers | Material | Transfer Orders and Related Utilities |
| SLTransNature2Alls | Vendor | Secondary Nature of Transaction Codes - All |
| SLTransNature2s | Codes | Secondary Nature of Transaction Codes |
| SLTransNatureAlls | Codes | Nature of Transaction Codes All |
| SLTransNatures | Codes | Nature of Transaction Codes |
| SLTrnacts | Material | Transfer Order Ship, Transfer Order Receive, and Combined TO Ship/Receive |
| SLTrnitemAlls | Material | Transfer Order Line Items and Related Utilities |
| SLTrnitems | Material | Transfer Order Line Items and Related Utilities |
| SLTrpHdrs | Material | Generate From Packing Slip |
| SLTrxRestrictCodeAlls | Material | Transaction Restriction Code All |
| SLTTApPosts | Vendor | A/P Voucher Posting |
| SLTTFinstmts | Finance | Temporary Table tt_finstmt |
| SLTTGlBanks | Vendor | Void Posted Draft Payments |
| SLTTInvAdjs | Customer | Interface to temporary table tt_inv_adj |
| SLTtJobtMatPosts | Product | Pending Job Material Transaction Posting |
| SLTTJournals | Finance | IDO for manipulating tt-journal with MassJournalPosting |
| SLTTPmtpcks | Customer | Interface to temporary table tt_pmtpck |
| SLTTTaxDists | Customer | Interface to temporary table tt_tax_dist |
| SLTTVouchers | Vendor | Permanent version of tt-voucher temp table (key includes connection_id) |
| SLTTVouchersFilterString | Vendor | Permanent version of tt-voucher temp table (key includes connection_id) |
| SLUMAlls | Codes | Unit of Measure Conversions All |
| SLUMConvs | Codes | Unit of Measure Conversions |
| SLUMs | Codes | Unit of Measure Codes |
| SLUnitcd1Alls | Finance | Unit Code 1 All |
| SLUnitcd1s | Finance | Unit Code 1 |
| SLUnitcd2Alls | Finance | Unit Code 2 All |
| SLUnitcd2s | Finance | Unit Code 2 |
| SLUnitcd3Alls | Finance | Unit Code 3 All |
| SLUnitcd3s | Finance | Unit Code 3 |
| SLUnitcd4Alls | Finance | Unit Code 4 All |
| SLUnitcd4s | Finance | Unit Code 4 |
| SLUnPostedTransactionsViews | Projects | UnPosted transaction tables row count |
| SLUserFormPreferences | Admin | User Form Preferences |
| SLUserLocals | Codes | Users - Additional Info tab |
| SLUserNames | Codes | Extends UserNames and includes user_local |
| SLVacations | Employee | Employee Vacation |
| SLVacParms | Employee | Vacation Parameters |
| SLVatObligations | Finance | MTD |
| SLVatProceduralMarkingAlls | Codes | Vat Procedural Marking Alls |
| SLVatProceduralMarkingDefaults | Codes | Vat Procedural Marking Default |
| SLVatProceduralMarkings | Codes | Vat Procedural Markings |
| SLVchHdrs | Vendor | Purge Voucher History |
| SLVchItemAlls | Vendor | Voucher Listing |
| SLVchPrAlls | Vendor | Posted Transaction - Voucher Pre-register |
| SLVchProceduralMarkingAlls | Codes | Voucher Procedural Markings - All |
| SLVchProceduralMarkings | Codes | Voucher Procedural Markings |
| SLVchPRs | Vendor | Vouchers Pre-Register |
| SLVchPrStaxAlls | Vendor | Voucher Pre-register Tax Distributions All |
| SLVchPrStaxs | Vendor | Voucher Pre-register Tax Distributions |
| SLVchStaxs | Vendor | vch_stax table information. Create for IDO Report. |
| SLVendaddrs | Vendor | Vendaddr table information |
| SLVendcatAlls | Vendor | Vendor Categories - All |
| SLVendCats | Vendor | Vendor Categories |
| SLVendConsignmentWhseItems | Material | Inventory Consigned From Vendor Receipt |
| SLVendLcrs | Vendor | Vendor Letters of Credit and Related Forms |
| SLVendOnTimeDelPercents | Vendor | Vendor On Time Delivery information |
| SLVendorAlls | Vendor | Vendors and Related Forms - All |
| SLVendorCertifications | Vendor | Vendor Certification |
| SLVendorCurrencies | Vendor | Vendor Currency Code |
| SLVendorMinorityTypeAlls | Vendor | Vendor Minority Type Alls |
| SLVendorMinorityTypes | Vendor | Vendor Minority Types |
| SLVendorPortalCompanyProfile | Vendor | Created for Vendor Portal - My Company Profile web page |
| SLVendorPortalItems | Material | IDO used only by the Vendor Portal |
| SLVendors | Vendor | Vendors and Related Forms |
| SLVendorSurchargeRules | Vendor | Vendor Surcharge Rules |
| SLVendorUsernames | Vendor | Vendor Usernames |
| SLVendTps | Vendor | EDI Vendor Profiles |
| SLW2TaxConss | Employee | W-2 States To Be Consolidated |
| SLWait000s | APS | 'Bound to WAIT000, an APS Scheduler output table used to record waiting time for the Planner" |
| SLWantAds | Employee | Want Ads |
| SLWaPoses | Employee | Want Ads - grid |
| SLWaUsage | Employee | Want Ad Usage |
| SLWBSAlls | Projects | Work Breakdown Structures for All Sites |
| SLWBSItemAlls | Projects | Work Breakdown Structures - Items Tab for All Sites |
| SLWBSItems | Projects | Work Breakdown Structures - Items Tab |
| SLWBSs | Projects | Work Breakdown Structures |
| SLWBSViews | Projects | Used by WBS Tree View - recursively |
| SLWcompAuthorities | Codes | Workers' Compensation Authority |
| SLWcompDCOs | Codes | Workers' Compensation Data Collection Organization |
| SLWcompInitialTreatments | Codes | Workers’ Compensation Initial Treatment Codes |
| SLWcompInjuryCodes | Codes | Workers’ Compensation Injury Codes |
| SLWcompInjuryGroups | Codes | Workers’ Compensation Injury Groups |
| SLWcompInsurers | Codes | Workers’ Compensation Insurer |
| SLWcompPolicies | Codes | Workers’ Compensation Policy |
| SLWcResourceGroups | Product | Job Operations - Co-products tab |
| SLWcs | Product | Work Centers |
| SLWhseAllRepRules | Material | Whse All For Replication Rules |
| SLWhseAlls | Material | Warehouses All |
| SLWhses | Material | Warehouses |
| SLWhseTransitTimes | Material | Warehouse Transit Times |
| SLYearToDateDeductionsandEarnings | Report | DataView for YearToDateDeductionsandEarnings |
| SLYearToDateDeductionsAndEarningsReport | Report | DataView for YearToDateDeductionsandEarnings |
