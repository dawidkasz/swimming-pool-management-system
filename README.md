# Swimming pool management system
Swimming pool management system created using [Django](https://www.djangoproject.com/),
[Bootstrap5](https://getbootstrap.com/) and [Charts.js](https://www.chartjs.org/).<br>
The main assumption is that this project should be used as an internal software and only the swimming pool employees should be<br>
allowed to make direct changes in the system. Interaction with the clients is accomplished by the **create reservation => pay for reservation** workflow.

Project contains 3 modules:
- **Tickets** - responsible for creating and paying for reservations.
- **Stats** - displays charts, which contain information about income, paid and unpaid reservations etc.<br>
  It can also generate a detailed report from a specific day.
- **Panel** - Allows full site configuration e.g. changing facility name, modyfing number of available swimlanes,<br>
  altering open/close time.

## See full documentation
### [Polish](docs/pl/index.md)