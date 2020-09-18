Known Bugs
===========

The function **graphvizToPng** which converts the dot file into an image using the subprocess module works only in a Linux environment
but not in Windows

.. code-block:: python

    def graphvizToPng(self, out_file):
        """
        Graphical rendering of the decision tree rules from the DOT file 

        :param out_file: Name of the output file
        :type out_file: String
        """
        outfile_path = os.path.join("results/", out_file)
        assert os.path.isfile(
            outfile_path), f"file {out_file!r} does not exist!"
        command = f"dot -Tpng {outfile_path} -o {outfile_path[:-4]}.png"
        try:
            subprocess.check_call(command, shell=True)
        except:
            print(f'Please run the following command in a Linux environment: \n {command}')
        else:
            print('Converting the dot file to png completed successfully!')
    
In order to overcome this problem, there are several solutions

    * An online tool_ can be used
    * An extension_ in VScode can be installed
    * A Linux subsystem can be installed in Windows. For further information, please check this link_

.. _tool: 
    https://onlineconvertfree.com/convert-format/dot-to-png/

.. _extension: 
    https://marketplace.visualstudio.com/items?itemName=joaompinto.vscode-graphviz

.. _link:
    https://docs.microsoft.com/en-us/windows/wsl/faq

