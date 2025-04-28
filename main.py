from services.db import CLIENTS, save_clients
from search import create_search_view
import flet as ft

def main(page: ft.Page):
    page.title = "Academy API Client"
    page.window.resizable = False
    page.window.width = 800
    page.window.height = 600
    page.bgcolor = "#cbc5d9"
    page.scroll = True

    def formatar_cpf(e):
        cpf = e.control.value
        cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
        if len(cpf) > 11:
            cpf = cpf[:11]
        if len(cpf) > 9:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        elif len(cpf) > 6:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
        elif len(cpf) > 3:
            cpf = f"{cpf[:3]}.{cpf[3:]}"
        e.control.value = cpf
        e.control.update()

    def register_client(e):
        name_value = name.value
        registration_value = registration.value
        plan_value = plan.value

        if not name_value or not registration_value or not plan_value:
            page.open(ft.SnackBar(
                content=ft.Text("Complete os campos!", size=16, color='black', weight='bold', font_family='Montserrat'),
                action="OK",
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                )
            )
            page.update()   
            return
        
        if plan_value == "Basic":
            expiration_value = 30
        elif plan_value == "Premium":
            expiration_value = 60
        elif plan_value == "Gold":
            expiration_value = 90
        elif plan_value == "VIP":
            expiration_value = 120

        new_client = {
            "name": name_value,
            "registration": registration_value,
            "plan": plan_value,
            "expiration": expiration_value,
            "id": len(CLIENTS) + 1,
        }
        
        CLIENTS.append(new_client)
        save_clients(CLIENTS)

        data_table.rows.append(
            ft.DataRow([
                ft.DataCell(ft.Text(new_client["id"], color='black')),
                ft.DataCell(ft.Text(new_client["name"], color='black')),
                ft.DataCell(ft.Text(new_client["registration"], color='black')),
                ft.DataCell(ft.Text(new_client["plan"], color='black')),
                ft.DataCell(ft.Text(new_client["expiration"], color='black')),
            ])
        )
        data_table.update()
    
        page.open(ft.SnackBar(
                content=ft.Text("Client registered successfully!", size=16, color='black', weight='bold', font_family='Montserrat'),
                action="OK",
                bgcolor="green",
                duration=ft.Duration(seconds=2),
            )
        )
        name.value = ""
        registration.value = ""
        plan.value = ""

        page.update()

    registration_clients = ft.Container(
        padding=20,
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=16),
        content=ft.Column(
            spacing=40,
            controls=[
                ft.Container(                    
                    content=ft.Row(
                        [
                            ft.Text("Register Client", size=30, weight=ft.FontWeight.BOLD, color="black", font_family='Montserrat'),
                        ],
                        alignment='center'
                    ),
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            name := ft.TextField(label="Name", width=350, border_color='black', color="black", label_style=ft.TextStyle(color="black")),
                            registration := ft.TextField(label="CPF", width=200, on_change=formatar_cpf, border_color='black', color="black", label_style=ft.TextStyle(color="black")),
                            plan := ft.Dropdown(
                                label="Plan",
                                options=[
                                    ft.dropdown.Option("Basic"),
                                    ft.dropdown.Option("Premium"),
                                    ft.dropdown.Option("Gold"),
                                    ft.dropdown.Option("VIP"),
                                ],
                                label_style=ft.TextStyle(color="black"),
                                text_style=ft.TextStyle(color="black"),                
                            ),
                            # expiration:= ft.TextField(label="Expiration (days)", width=150, border_color='black', color="black", label_style=ft.TextStyle(color="black")),
                        ],
                        alignment='center',
                    ),
                ),
                ft.Row(
                    alignment='center',
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10, top=-5),
                            content=ft.ElevatedButton(
                                "Submit", width=100, on_click=register_client, color='#cbc5d9'
                            ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10, top=-5),
                            content=ft.ElevatedButton(
                                "Clear", width=100, on_click=lambda e: [name.update(value=""), registration.update(value=""), plan.update(value="")], color='#cbc5d9'
                            ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10, top=-5),
                            content=ft.ElevatedButton(
                                "Search", width=100, on_click=create_search_view, color='#cbc5d9'
                            )
                        )
                    ]
                )
            ],
        ),
    )

    clients = ft.Container(
        # bgcolor='white',
        padding=ft.padding.only(top=-10),
        margin=ft.margin.only(top=-15),
        alignment=ft.alignment.center,
        content=ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                spacing=20,
                alignment='center',
                controls=[
                    ft.Row(
                        [
                            ft.Text("Registered Clients", size=30, weight=ft.FontWeight.BOLD, color='black', font_family='Montserrat'),
                        ],
                        alignment='center',
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            [
                                data_table:=ft.DataTable(
                                    width=750,
                                    columns=[
                                        ft.DataColumn(ft.Text("ID", color='black', size=16)),
                                        ft.DataColumn(ft.Text("Name", color='black', size=16)),
                                        ft.DataColumn(ft.Text("CPF", color='black', size=16)),
                                        ft.DataColumn(ft.Text("Plan", color='black', size=16)),
                                        ft.DataColumn(ft.Text("Expiration (days)", color='black', size=16)),
                                    ],
                                    rows=[
                                        ft.DataRow([
                                            ft.DataCell(ft.Text(client["id"], color='black')),
                                            ft.DataCell(ft.Text(client["name"], color='black')),
                                            ft.DataCell(ft.Text(client["registration"], color='black')),
                                            ft.DataCell(ft.Text(client["plan"], color='black')),
                                            ft.DataCell(ft.Text(client["expiration"], color='black')),
                                        ]) for client in CLIENTS
                                    ],                        
                                ),
                            ]
                        )
                    )
                ],
            ),
        ),
    )

    page.add(
        registration_clients,
        clients,
    )

    page.update()

ft.app(target=main)