from tkinter import *
from tkinter import ttk
import sys

try:
    import netaddr
except ImportError:
    print("No module named 'netaddr'")
    sys.exit()

def calculate_Subnet():
    data = network_Entry.get()
    if len(data) == 0:
        network_Entry.configure(background="red", highlightcolor="red")
    else:
        network_Entry.configure(background="white",highlightbackground="blue", highlightcolor="blue")

    try:
        ip_network = netaddr.IPNetwork(data)

        if ip_network.version == 4:
            broadcast_Value.set(ip_network.broadcast)
            netmask_Value.set(ip_network.netmask)
            hostmask_Value.set(ip_network.hostmask)

            if ip_network.size > 4:
                Size = '('+str(ip_network.size - 3)+')'
                size_Value.set("{} Usable Addresses".format(Size))
            else:
                size_Value.set("(1) Usable Address")

            ipaddr_Text.delete(1.0, END)

            ip_network_Values = []
            for ipaddr in list(ip_network):
                ip_network_Values.append(str(ipaddr))

            if len(ip_network_Values) > 2:
                ip_network_Values.pop(0)
                ip_network_Values.pop()
            gateway_Value.set(ip_network_Values.pop(0))

            if len(ip_network_Values) == 0:
                ip_network_Values.append(gateway_Value.get())

            ipaddr_Text.insert(END,"\tUsable Addresses\n")
            ipaddr_Text.insert(END, '\n'.join(ip_network_Values))
            status_Value.set("Calculated")

        else:
            status_Value.set("IPv6 Networks Not Supported")

    except netaddr.AddrFormatError:
        status_Value.set("Invalid Network")

def on_leave(e):
    calculate_Button['background'] = 'gray60'

def on_click(event):
    network_Entry.delete(0, END)



if __name__ == "__main__":

    Window = Tk()
    Window.title("Subnet Calculator")
    Window.resizable(0, 0)
    Window.configure(bg='gray80')

# ============================  creating string widget variables ====================================
    broadcast_Value = StringVar()
    netmask_Value = StringVar()
    hostmask_Value = StringVar()
    size_Value = StringVar()
    gateway_Value = StringVar()
    status_Value = StringVar()

    size_Value.set("(0) Usable Addresses")

    broadcast_Label = Label(Window, text="Broadcast")
    broadcast_Value_Text = Entry(Window, state='readonly', width=15)
    broadcast_Value_Text.config(textvariable=broadcast_Value)
    netmask_Label = Label(Window, text="Netmask")
    netmask_Value_Text = Entry(Window, state='readonly', width=15)
    netmask_Value_Text.config(textvariable=netmask_Value)
    hostmask_Label = Label(Window, text="Hostmask")
    hostmask_Value_Text = Entry(Window, state='readonly', width=15)
    hostmask_Value_Text.config(textvariable=hostmask_Value)
    size_Label = Label(Window, textvariable=size_Value, bg ="gray60")
    gateway_Label = Label(Window, text="Gateway")
    gateway_Value_Text = Entry(Window, state='readonly', width=15)
    gateway_Value_Text.config(textvariable=gateway_Value)
    ipaddr_Scrollbar = Scrollbar(Window, bg ="gray60")
    ipaddr_Text = Text(Window, width=30, height=10, yscrollcommand=ipaddr_Scrollbar.set)
    ipaddr_Scrollbar.config(command=ipaddr_Text.yview)
    status_Value_Label = Label(Window, textvariable=status_Value, relief=SUNKEN, bg ="gray60")
    network_Entry = Entry(Window, width=15, relief="solid")
    calculate_Button = Button(Window, text="Calculate", width=15, command=calculate_Subnet, bg ="gray60", relief="solid")
    separator = ttk.Separator(Window, orient='horizontal')
    separator2 = ttk.Separator(Window, orient='horizontal')

# ==================================  adding widgets to grid =======================================
    calculate_Button.grid(row=0, column=0)
    network_Entry.grid(row=0, column=1)

    separator.grid(row=1,column=0,columnspan=2, ipadx=150, ipady=1)

    gateway_Label.grid(row=2, column=1)
    gateway_Value_Text.grid(row=2, column=0)
    netmask_Label.grid(row=3, column=1)
    netmask_Value_Text.grid(row=3, column=0)
    hostmask_Label.grid(row=4, column=1)
    hostmask_Value_Text.grid(row=4, column=0)
    broadcast_Label.grid(row=5, column=1)
    broadcast_Value_Text.grid(row=5, column=0)

    separator2.grid(row=6,column=0,columnspan=2, ipadx=150, ipady=1)

    size_Label.grid(row=7, column=0, columnspan=2, sticky=W + E)
    ipaddr_Text.grid(row=8, column=0, columnspan=2, sticky=W + E)
    ipaddr_Scrollbar.grid(row=8, column=2, sticky=N + S)
    status_Value_Label.grid(row=9, column=0, columnspan=3, sticky=W + E)

# ==================================  adding placeholder =======================================
    network_Entry.insert(0, "Network Address")


    calculate_Button.bind("<Leave>", on_leave)
    network_Entry.bind('<Button-1>', on_click)

    Window.mainloop()
