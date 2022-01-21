# Famcy Quick Start
This goes through an example to show how to quickly develop a page via Famcy framework.

## Start a new project
### Setup Famcy YAML

| Variable Name 				| Description 										| Example |
| ----------------------------- | ------------------------------------------------- | ---------- |
| console_title 				| Name of the website 								| console_title: "Famcy Example" |
| console_description			| Description of the website 						| console_description: "This is an example" |
| main_page						| Connect default route "/" 						| main_page: overview |
| side_bar_title 				| Title of side bar and its endpoint is "/" 		| side_bar_title: "dashboard" |
| side_bar_hierachy				| Connect side bar title and endpoint 				| side_bar_hierachy:<br>	+ 總覽: overview<br>	+ 車輛管理: car_management<br>	+ 月票管理: season<br>	+ POS功能: pos<br>	+ 財務功能: finance |
| title_style					| Icon of title button of side bar 					| title_style: "bxs-spreadsheet"<br><b>[Icon library (version 2.0.8) => https://boxicons.com/]<b> |
| side_bar_style 				| Icons of buttons of side bar 						| side_bar_style:<br>	總覽: "bxs-share-alt"<br>	車輛管理: "bxs-car-mechanic"<br>	月票管理: "bxs-calendar"<br>	POS功能: "bx-desktop"<br>	財務功能: "bx-trending-up"<br><b>[Icon library (version 2.0.8) => https://boxicons.com/]<b> |
| main_url 						| Url of current website 							| main_url: "http://127.0.0.1:5000" |
| with_login					| Flag of login requirement of the website 			| with_login: True |
| login_url						| Endpoint of login page 							| login_url: "iam/login" |
| default_name					| Default user name 								| default_name: "Famcy" |
| default_profile_pic_url		| Default user picture 								| default_profile_pic_url: "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fchannel%2FUClOgrSn4afPVICckeKLc21g&psig=AOvVaw2NbtZ9PmMyfu9t9KZmXCvZ&ust=1635439303581000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIiBgKiE6_MCFQAAAAAdAAAAABAD" |
| 【Http Client】					| Http url the the developer may use in the project | eg.<br>main_http_url: "http://127.0.0.2:8000"<br>login_http_url: "http://127.0.0.3:8000" |

### Correctly setup folder hierarchy under console folder
Folder names that start with `_` won't be imported by Famcy, or else objects can be called in the project by writing `Famcy.<object name>`. Customize javascript, image of css files can be used in the project after including those files in the `_static_` folder.

	  console
		|__ _static_
		|   |__css
		|   |__image
		|   |__js
		|
		|__page1
		|   |__page.py
		|
		|__page2
		|   |__page.py
		|
		|__iam
			|__page.py

### Create a page and connect it with a unique endpoint
