---
name: find-business-owner-name
display_name: "Find Business Owner Name"
description: Identifies the full name of a business owner using provided inputs.
category: productivity
icon: user
skill_type: sandbox
catalog_type: addon
resource_requirements:
  - env_var: HUNTERIO_API_KEY
    name: Hunter.io API Key
    description: API key for accessing the Hunter.io API.
tool_schema:
  type: object
  properties:
    placeId:
      type: string
      description: Google Maps placeId of the business.
    website:
      type: string
      description: Website of the business.
    address:
      type: string
      description: Address of the business.
    business_name:
      type: string
      description: Name of the business.
  required: []
---
# Find Business Owner
Identifies the full name of a business owner using provided inputs.