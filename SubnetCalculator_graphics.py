#--------------------------------
# TIE-51107 Subnet Calculator
# Tomi Mannila 
# --------
# Subnet Calculator
# Calculates subnet mask, network address,
# broadcast address and available hosts
#--------------------------------

import ipaddress
import textwrap
from tkinter import *


#User interface
class Kayttoliittyma:

    def __init__(self):
        # Class builder

        # Introduce all the elements
        self.__pääikkuna = Tk()
        self.__pääikkuna.title("Subnet calculator")

        self.__IP_ohje = Label(self.__pääikkuna, text="Enter the IP address with subnet.")
        self.__IP_esim = Label(self.__pääikkuna, text="( e.g. 192.168.1.1 /24 )")
        self.__IP_laskeButton = Button(self.__pääikkuna, text="Calc", command=self.Laske)
        self.__IP_txt = Label(self.__pääikkuna, text="IP: ")
        self.__IP = Entry(width=19, justify="center")

        self.__ilmoitus = Label(self.__pääikkuna, text="")

        self.__NetworkAddress_text = Label(self.__pääikkuna, text="Network Address:")
        self.__NetworkAddress = Entry(self.__pääikkuna, text="", justify="center")
        self.__NetworkAddress.configure(state="readonly", width=29)

        self.__SubnetMask_text = Label(self.__pääikkuna, text="Subnet Mask:")
        self.__SubnetMask = Entry(self.__pääikkuna, text="", justify="center")
        self.__SubnetMask.configure(state="readonly", width=29)

        self.__BroadcastAddress_text = Label(self.__pääikkuna, text="Broadcast Address:")
        self.__BroadcastAddress = Entry(self.__pääikkuna, text="", justify="center")
        self.__BroadcastAddress.configure(state="readonly", width=29)

        self.__AvailableHosts_text = Label(self.__pääikkuna, text="Available Hosts:")
        self.__AvailableHosts = Entry(self.__pääikkuna, text="", justify="center")
        self.__AvailableHosts.configure(state="readonly", width=29)

        self.__lopeta_button = Button(self.__pääikkuna, text="Exit", command=self.Lopeta)


        # Place to grid
        self.__IP_ohje.grid(row=1, column=1, sticky=N+E+S+W)
        self.__IP_esim.grid(row=2, column=1, sticky=N)
        self.__IP_txt.grid(row=3, column=0, sticky=W)
        self.__IP.grid(row=3, column=1, sticky=W+E+S+N)

        self.__IP_laskeButton.grid(row=3, column=2, sticky=E)

        self.__ilmoitus.grid(row=4, column=1, sticky=N+S+E+W)

        self.__NetworkAddress_text.grid(row=5, column=1, sticky=N)
        self.__NetworkAddress.grid(row=6, column=1, sticky=N)

        self.__SubnetMask_text.grid(row=7, column=1, sticky=N)
        self.__SubnetMask.grid(row=8, column=1, sticky=N)

        self.__BroadcastAddress_text.grid(row=9, column=1, sticky=N)
        self.__BroadcastAddress.grid(row=10, column=1, sticky=N)

        self.__AvailableHosts_text.grid(row=11, column=1, sticky=N)
        self.__AvailableHosts.grid(row=12, column=1, sticky=N)

        self.__lopeta_button.grid(row=13, column=2, sticky=E)



        # Properties of the window
        self.__pääikkuna.geometry("300x300")

        self.__pääikkuna.mainloop()


    def Lopeta(self):
        # End the program
        self.__pääikkuna.destroy()

    def ShowHosts(self, network, maskInt):
        # Calculate available hosts

        # list of all available hosts
        availableHosts = list(network.hosts())

        firstHost = availableHosts[0]
        lastHost = availableHosts[len(availableHosts)-1]
        if (maskInt != 31) and (maskInt != 32):

            hosts = str(firstHost)+" - "+str(lastHost)

            # AvailableHosts's state is "readonly". Thus, state="normal"
            # needs to be stated before modifying.
            self.__AvailableHosts.configure(state="normal")
            self.__AvailableHosts.delete(0, END)
            self.__AvailableHosts.insert(0, hosts)
            self.__AvailableHosts.configure(state="readonly")


        else:
            print ('Not enough room for hosts.')

        availableHosts.clear()


    def GenerateNetworkAddress(self, ipandmask):
        # Generate network and broadcast address from input
        # strict=False because host bits are used

        networkAddress = ipaddress.ip_network(ipandmask, strict=False)

        # generate broadcast address from networkAddress -object
        broadcastAddress = networkAddress.broadcast_address

        self.__NetworkAddress.configure(state="normal")
        self.__NetworkAddress.delete(0, END)
        self.__NetworkAddress.insert(0, networkAddress)
        self.__NetworkAddress.configure(state="readonly")

        self.__BroadcastAddress.configure(state="normal")
        self.__BroadcastAddress.delete(0, END)
        self.__BroadcastAddress.insert(0, broadcastAddress)
        self.__BroadcastAddress.configure(state="readonly")

        return networkAddress

    def GenerateMask(self, maskInt):
        # Generate mask from prefix form

        mask = [00000000, 00000000, 00000000, 00000000]
        zeros = 32 - maskInt
        maskBit = ("1" * maskInt) + ("0" * zeros)

        maskBitWrapped = textwrap.wrap(maskBit, 8)

        for x in range(0, 4):

            partMask = int(maskBitWrapped[x], 2)
            mask[x] = partMask

        maskString = str(mask[0])+"."+str(mask[1])+"."+str(mask[2])+"."+str(mask[3])

        self.__SubnetMask.configure(state="normal")
        self.__SubnetMask.delete(0, END)
        self.__SubnetMask.insert(0, maskString)
        self.__SubnetMask.configure(state="readonly")

        mask = [00000000, 00000000, 00000000, 00000000]

    def Laske(self):
        # Start the calculations

        self.__ilmoitus["text"] = ""
        userInput = self.__IP.get()

        if userInput == "":
            return

        userInput = userInput.replace(" ", "")

        #Separate ip and mask index 0 is ip and index 1 is mask
        ipfromstring = userInput.split("/")
        ipfromstring[0] = ipfromstring[0].strip()


        try:
            IP = ipaddress.ip_address(ipfromstring[0])

            #Get mask
            maskInt = int(ipfromstring[1])

            if 0 <= maskInt <= 32:

                self.GenerateMask(maskInt)

                network = self.GenerateNetworkAddress(userInput)

                self.ShowHosts(network, maskInt)

                userInput = ""

            else:
                userInput = ""
                raise ValueError

        except:
            userInput = ""
            self.__ilmoitus["text"] = "Unexpected error. Please, check your input."

            #self.__NetworkAddress["text"] = ""
            self.__NetworkAddress.configure(state="normal")
            self.__NetworkAddress.delete(0, END)
            self.__NetworkAddress.configure(state="readonly")

            #self.__BroadcastAddress["text"] = ""
            self.__BroadcastAddress.configure(state="normal")
            self.__BroadcastAddress.delete(0, END)
            self.__BroadcastAddress.configure(state="readonly")

            #self.__AvailableHosts["text"] = ""
            self.__AvailableHosts.configure(state="normal")
            self.__AvailableHosts.delete(0, END)
            self.__AvailableHosts.configure(state="readonly")

            #self.__SubnetMask["text"] = ""
            self.__SubnetMask.configure(state="normal")
            self.__SubnetMask.delete(0, END)
            self.__SubnetMask.configure(state="readonly")


def main():

    kali = Kayttoliittyma()


main()
