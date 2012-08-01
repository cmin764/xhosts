#
# ui:   user interface module for graphical handling
# Copyright (C) 2012  cmiN
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Cosmin Poieana <cmin764@yahoo.com>


from Tkinter import * # it's evil, I know ;[
from tkMessageBox import showinfo # for About


# some constants
BWD = 4 # button width
SEP = "->" # separator between source and destination


class Gui(Frame):

    def __init__(self, master=Tk(), margin=10, core=None):
        """Create toplevel and grid the frame on it."""
        Frame.__init__(self, master)
        self.core = core # the application engine
        self.master.title("xhosts")
        self.grid(padx=margin, pady=margin)
        self.widgets()
        self.reloadButton.invoke() # press Reload

    def widgets(self):
        """Crate and grid other widgets."""
        # create widgets
        self.hostsBox = Listbox(self, width=30, height=5)
        self.hostsBox.bind("<<ListboxSelect>>", self.select_host)
        self.hostsScroll = Scrollbar(self, command=self.hostsBox.yview,
                                     orient=VERTICAL)
        self.hostsBox.config(yscrollcommand=self.hostsScroll.set)
        self.srcEntry = Entry(self, width=15)
        self.destEntry = Entry(self, width=15)
        self.about = Label(self, text="A\nb\no\nu\nt", bg="orange")
        self.about.bind("<Button-1>", self.about_message)
        self.reloadButton = Button(self, text="Reload", width=BWD,
                                   command=self.reload_hosts)
        self.saveButton = Button(self, text="Save", width=BWD,
                                 command=self.save_hosts)
        self.addButton = Button(self, text="Add", width=BWD,
                                command=self.add_host)
        self.removeButton = Button(self, text="Remove", width=BWD,
                                   command=self.remove_host)
        self.searchEntry = Entry(self, width=20)
        self.searchButton = Button(self, text="Search", width=BWD)
        self.searchBox = Listbox(self, height=5)
        self.searchScroll = Scrollbar(self, command=self.searchBox.yview,
                                      orient=VERTICAL)
        self.searchBox.config(yscrollcommand=self.searchScroll.set)
        # grid (place and show) widgets
        self.hostsBox.grid(row=0, column=0, columnspan=2, sticky=W + E)
        self.hostsScroll.grid(row=0, column=2, sticky=N + S)
        self.srcEntry.grid(row=1, column=0, sticky=W)
        self.destEntry.grid(row=1, column=1, sticky=W)
        self.about.grid(row=1, column=2, rowspan=3, sticky=N + S + W + E)
        self.reloadButton.grid(row=2, column=0, sticky=W)
        self.saveButton.grid(row=2, column=0, sticky=E)
        self.addButton.grid(row=2, column=1, sticky=W)
        self.removeButton.grid(row=2, column=1, sticky=E)
        self.searchEntry.grid(row=3, column=0, columnspan=2, sticky=W)
        self.searchButton.grid(row=3, column=1, sticky=E)
        self.searchBox.grid(row=4, column=0, columnspan=2, sticky=W + E)
        self.searchScroll.grid(row=4, column=2, sticky=N + S)

    def about_message(self, event):
        """Show this when About is clicked."""
        showinfo("About", "Show and edit entries from hosts file, " \
                 "also search for hostnames on the web. Coded by cmiN.\n\n" \
                 "\t Visit rstcenter.com")

    def __clear_entries(self):
        """Empty the src and dest entry."""
        self.srcEntry.delete(0, END)
        self.destEntry.delete(0, END)

    def __get_selected_host(self):
        """Return selected host's index."""
        crtTuple = self.hostsBox.curselection()
        if len(crtTuple):
            return crtTuple[0]
        return None

    def select_host(self, event):
        """Display the selected host in the entries below."""
        index = self.__get_selected_host()
        item = self.hostsBox.get(index).split(SEP) # split item
        self.__clear_entries()                     # in src and dest
        self.srcEntry.insert(0, item[0].strip())
        self.destEntry.insert(0, item[1].strip())

    def reload_hosts(self):
        """Reload and display hosts."""
        self.__clear_entries()
        self.hostsBox.delete(0, END)
        for item in self.core.list_entries():
            self.hostsBox.insert(END, "%s {} %s".format(SEP) % item)

    def save_hosts(self):
        """Save the current entries to hosts file."""
        self.core.write_entries()

    def add_host(self):
        """Add host (from src and entry) to memory and listbox."""
        src = self.srcEntry.get().strip()
        dest = self.destEntry.get().strip()
        if not bool(src) or not bool(dest):
            return # empty src or dest
        rcode = self.core.add_entry(src, dest) # add to memory
        item = "%s {} %s".format(SEP) % (src, dest)
        if rcode == 1: # added
            self.hostsBox.insert(END, item)
        else: # replaced
            # find and replace in the listbox too
            for index in xrange(self.hostsBox.size()):
                crt = self.hostsBox.get(index).split(SEP)
                if src == crt[0].strip():
                    # replace the item
                    self.hostsBox.delete(index)
                    self.hostsBox.insert(index, item)
                    break

    def remove_host(self):
        """Remove host from both memory and listbox."""
        index = self.__get_selected_host() # may be None here
        if index: # something is selected, remove it
            item = self.hostsBox.get(index).split(SEP)
            self.core.remove_entry(item[0].strip())
            self.hostsBox.delete(index)
