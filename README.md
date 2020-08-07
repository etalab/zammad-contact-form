# zammad-contact-form

## Configuration

### Z_TOKEN

`Z_TOKEN` env var should be set with a valid Zammad API token (permissions: `report`, `ticket.agent`).

### Z_URL

`Z_URL` env var should be set with the Zammad API base URL, e.g. https://support.etalab.gouv.fr/api/v1.

### Ticket categories

Set as a list in `src/config.js`. Each item should be:

```
{ value: '<name-of-zammad-group>', text: '<option-text-in-form>', description: "<description-in-form>" }
```

`<name-of-zammad-group>` is used to assign the ticket to the right group in Zammad.
