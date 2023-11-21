# The simplified VPN service

### Author - Ihor Prokopenko:
 - Email: i.prokopenko.dev@gmail.com
 - LinkedIn: https://www.linkedin.com/in/i-prokopenko/

### Overview
This project is a Django web application that provides a VPN-like service for accessing external sites through a proxy. It includes user authentication, site registration, and proxy functionality.

### Key Features
1. Proxy Functionality: Allows users to access external sites through a proxy by specifying the site name and optional path.

2. User Authentication: Users can register, log in, and log out. Only authenticated users can use the proxy and access certain features.

3. Site Registration: Users can register their favorite sites, providing a base URL for proxy access.

4. Profile Management: Users have a profile page displaying relevant information and can edit their profile details.

5. Site Deletion: Users can delete registered sites from their profile.


### Setup

1. Clone project from GitHub repository:
   - `git clone https://github.com/Ihor-Prokopenko/simplified-VPN-test-task.git` 
2. Make sure You have installed and launched Docker.
3. Follow to the project dir in your teminal and run the next commands:
    - `docker-compose build`
    - `docker-compose up`
4. Now You can try it at the next url - http://localhost:8000/
    - The admin user creating automaticly so you can login with (username=admin, password=admin) credentials.
    - Or just create new user - http://localhost:8000/register/


