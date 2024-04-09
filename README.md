# drf_project
Project for group fundraising.

Steps for set up project.

0. Clone in some_folder repository by command 'git clone https://github.com/Gjkan/drf_group_fundraising.git'
1. Create file .env.dev in some_folder/django/group_fundraising/docker/env. 
2. Write down project variables in .env.dev using template from file some_folder/django/group_fundraising/docker/env/.env.template.
3. Open cmd and go to some_folder/django/group_fundraising.
4.  Build image. Write in cmd command 'docker compose -f docker-compose.dev.yml build'. Press enter.
5. Write in cmd command 'docker compose -f docker-compose.dev.yml up' being in the same folder as in step 4. Press enter.
6. Url 'localhost/api' in browser open group_fundraising api overview.