# Agent Outreach

Use these tools to inspect your own TopYappers outreach agent projects and email history. They are designed for inbox workflows where you only have a creator's email address and need to understand what was sent before drafting a reply.

## Tools

| Tool | Endpoint | Cost |
|------|----------|------|
| `list_agent_projects` | `GET /api/v1/agent/projects` | Free |
| `list_contacted_creators` | `GET /api/v1/agent/contacted-creators` | Free |
| `list_agent_messages` | `GET /api/v1/agent/messages` | Free |

## Common reply workflow

1. Call `list_contacted_creators` with `creatorEmail` set to the email address from the inbox.
2. Call `list_agent_messages` with the same `creatorEmail` and `direction: "all"`.
3. Call `list_agent_projects` if you need project targeting, deal terms, or custom instructions.
4. Use the original pitch, follow-ups, inbound replies, and project context to draft a customized response.

## list_agent_projects

Returns active outreach projects with campaign settings, target keywords, target countries, deal config, message overrides, and counters.

### Parameters

No parameters.

## list_contacted_creators

Returns creators who received at least one non-failed outbound email.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectId` | string | Filter to one agent project. |
| `creatorEmail` | string | Case-insensitive exact creator email match. |
| `creatorEmailContains` | string | Case-insensitive partial creator email match. |
| `creatorId` | string | Filter by creator ID. |
| `page` | integer | Page number, default 1. |
| `perPage` | integer | Results per page, default 50, max 100. |

### Useful response fields

- `creator_email`, `creator_id`, `creator_name`, `creator_platform`
- `project_ids`, `thread_ids`
- `sent_messages_count`, `reply_messages_count`, `has_replies`
- `first_contacted_at`, `last_contacted_at`, `last_reply_at`
- `last_subject`, `last_status`, `last_body_preview`

## list_agent_messages

Returns saved agent email messages, including outbound emails and inbound creator replies.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectId` | string | Filter to one agent project. |
| `creatorEmail` | string | Case-insensitive exact creator email match. |
| `creatorEmailContains` | string | Case-insensitive partial creator email match. |
| `creatorId` | string | Filter by creator ID. |
| `threadId` | string | Filter by Gmail thread ID. |
| `gmailAccountId` | string | Filter by connected Gmail account ID. |
| `direction` | string | `all`, `outbound`, or `inbound`. Default: `all`. |
| `status` | string | Filter by message status, such as `sent`, `received`, `replied`, or `failed`. |
| `isFollowUp` | boolean | Filter follow-up emails. |
| `page` | integer | Page number, default 1. |
| `perPage` | integer | Results per page, default 50, max 100. |

### Useful response fields

- `project_id`, `conversation_id`
- `sender_email`, `direction`
- `creator_id`, `creator_name`, `creator_email`, `creator_platform`
- `subject`, `body`, `body_preview`
- `status`, `thread_id`, `message_id`, `parent_message_id`
- `sent_at`, `replied_at`, `failed_at`, `date_created`
