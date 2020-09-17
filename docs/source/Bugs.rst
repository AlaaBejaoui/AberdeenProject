Known Bugs
===========

The function **graphvizToPng** which converts the dot file into an image using the subprocess module works perfectly in Linux but not in Windows

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
        subprocess.call(command, shell=True)
    
In order to overcome this problem, an online tool_ can be used or an extension_ in VScode can be installed

.. _tool: 
    https://onlineconvertfree.com/convert-format/dot-to-png/

.. _extension: 
    https://marketplace.visualstudio.com/items?itemName=joaompinto.vscode-graphviz

