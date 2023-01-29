import flet as ft
from db import *

def main(page: ft.Page):

    #Page initialization

    page.window_height = 600
    page.window_width = 400
    page.title = "MyPass Manager"
    page.scroll = "auto"

    page.on_connect = initialize_db()

    #Controls Logic

    def handle_search_change(e):
        if switch_row[1].value == False:
            handle = search_box.value
            results = get_by_handle(handle)
            my_data[0] = my_data_table(data=results)
            page.update()

        if switch_row[1].value == True:
            service = search_box.value
            results = get_by_service(service)
            my_data[0] = my_data_table(data=results)
            page.update()

    def handle_new_pass(service, account):

        def open_dlg(*e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def close_dlg(*e):
            dlg_modal.open = False
            page.update()

        def submit(*e):
            password = new_password_field.value
            create_pass(service, account, password)
            close_dlg()

        new_password_field = ft.TextField(label="New Password", width=200, height=40)

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Enter {account} Passcode?"),
            content=new_password_field,
            actions=[ft.Row(
                [
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("Submit", on_click=submit)
                ]
                )
                ]
        )

        open_dlg()

    def handle_account_click(password):
        page.set_clipboard(password)

    def handle_account_long_press(my_id, account):

        def close_dlg(*e):
            dlg_modal.open = False
            page.update()

        def open_dlg(*e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def edit_entry(e):
            password = change_password_field.value
            change_pass(my_id, password)
            close_dlg()

        def delete_entry(e):
            delete_pass(my_id)
            close_dlg()


        change_password_field = ft.TextField(label="Change Password", width=200, height=40)

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Edit {account} Passcode?"),
            content=change_password_field,
            actions=[ft.Row(
                [ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("Delete", on_click=delete_entry),
                ft.TextButton("Submit", on_click=edit_entry)], spacing=0)
            ]
        )

        open_dlg()

    #Controls Display

    def my_data_table(data=None):
        
        add_service = ft.TextField(label="Add Service", height=45)
        add_account = ft.TextField(
            label="Add Account",
            on_submit=lambda _: handle_new_pass(add_service.value, add_account.value),
            height=45
        )

        default = ft.DataRow(cells = [
            ft.DataCell(add_service),
            ft.DataCell(add_account)
        ])

        data_rows = [default]


        if data != None:
            data_rows = [default]
            for entry in data:
                my_id=entry[0]
                service=entry[1]
                account=entry[2]
                password=entry[3]
                
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(service)),
                        ft.DataCell(ft.TextButton(
                            account,
                            on_click=lambda _: handle_account_click(password),
                            on_long_press=lambda _: handle_account_long_press(my_id, account)
                        ))
                    ]
                )
            
                data_rows.append(row)

        table = ft.DataTable(
            width=350,
            column_spacing=5,
            columns=[
                ft.DataColumn(ft.Text("Service")),
                ft.DataColumn(ft.Text("Account"))
            ],
            rows = data_rows
        )
        return table

    header = ft.Text("Welcome to MyPass")
    search_box = ft.TextField(
            label="Search",
            width=250, height=40,
            suffix_icon=ft.icons.SEARCH,
            on_change=handle_search_change)
    switch_row = [ft.Text("Account"), ft.Switch(value=False), ft.Text("Service")]

    my_data = [my_data_table()]

    page.add(
        ft.Row([header], alignment="center"),
        ft.Row([search_box], alignment="center"),
        ft.Row(switch_row, alignment="center"),
        ft.Row(my_data, alignment="center")
    )

ft.app(target=main)
