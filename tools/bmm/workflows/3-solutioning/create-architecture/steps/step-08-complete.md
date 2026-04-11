# Step 8: Architecture Completion & Handoff

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER generate content without user input

- 📖 CRITICAL: ALWAYS read the complete step file before taking any action - partial understanding leads to incomplete decisions
- ✅ ALWAYS treat this as collaborative completion between architectural peers
- 📋 YOU ARE A FACILITATOR, not a content generator
- 💬 FOCUS on successful workflow completion and implementation handoff
- 🎯 PROVIDE clear next steps for implementation phase
- ⚠️ ABSOLUTELY NO TIME ESTIMATES - AI development speed has fundamentally changed
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis before taking any action
- 🎯 Present completion summary and implementation guidance
- 📖 Update frontmatter with final workflow state
- 🚫 THIS IS THE FINAL STEP IN THIS WORKFLOW

## YOUR TASK:

Complete the architecture workflow, provide a comprehensive completion summary, and guide the user to the next phase of their project development.

## COMPLETION SEQUENCE:

### 1. Congratulate the User on Completion

Both you and the User completed something amazing here - give a summary of what you achieved together and really congratulate the user on a job well done.

### 2. Update the created document's frontmatter

```yaml
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '{{current_date}}'
```

### 3. Publish to Confluence and Create Jira Issues

**Remote Output Publishing:**

Read fully and execute: `{project-root}/_bmad/bmm/tasks/remote-output-push.md`

This will offer to:
- Publish the completed architecture document to Confluence under Feature Grooming (space: `{confluence_publish_space}`, parent: `{confluence_feature_grooming_page_id}`)
- Apply labels: `architecture,bmad-generated`
- Create Jira epics in project `{jira_project}` derived from the architecture's implementation phases (optional)
- Check for existing pages/issues before creating duplicates

Present options [P] Confluence / [J] Jira Epics / [B] Both / [S] Skip and wait for user selection before proceeding.

### 4. Next Steps Guidance

Architecture complete. Read fully and follow: `{project-root}/_bmad/core/tasks/help.md`

Upon Completion of task output: offer to answer any questions about the Architecture Document.


## SUCCESS METRICS:

✅ Complete architecture document delivered with all sections
✅ All architectural decisions documented and validated
✅ Implementation patterns and consistency rules finalized
✅ Project structure complete with all files and directories
✅ User provided with clear next steps and implementation guidance
✅ Workflow status properly updated
✅ User collaboration maintained throughout completion process

## FAILURE MODES:

❌ Not providing clear implementation guidance
❌ Missing final validation of document completeness
❌ Not updating workflow status appropriately
❌ Failing to celebrate the successful completion
❌ Not providing specific next steps for the user
❌ Rushing completion without proper summary

❌ **CRITICAL**: Reading only partial step file - leads to incomplete understanding and poor decisions
❌ **CRITICAL**: Proceeding with 'C' without fully reading and understanding the next step file
❌ **CRITICAL**: Making decisions without complete understanding of step requirements and protocols

## WORKFLOW COMPLETE:

This is the final step of the Architecture workflow. The user now has a complete, validated architecture document ready for AI agent implementation.

The architecture will serve as the single source of truth for all technical decisions, ensuring consistent implementation across the entire project development lifecycle.
