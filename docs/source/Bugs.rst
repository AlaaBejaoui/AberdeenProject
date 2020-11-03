.. _limitations:

Limitations
===========

Windows bugs
-------------

The function **graphvizToPng** which converts the dot file into an image using the subprocess module works only in a
Linux environment but not in Windows

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

    * An `online tool <https://onlineconvertfree.com/convert-format/dot-to-png/>`__ can be used
    * An `extension <https://marketplace.visualstudio.com/items?itemName=joaompinto.vscode-graphviz>`__ in VScode can be installed
    * A Linux subsystem can be installed in Windows. For further information, please check the following links

        * `How to install the Linux subsystem in Windows 10 ? <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__
        * `How to find the Windows files in the Linux subsystem ? <https://docs.microsoft.com/en-us/windows/wsl/faq#how-do-i-use-a-windows-file-with-a-linux-app>`__

Imbalanced classes
------------------
During our tests with the Aberdeen data, we encountered the problem of imbalanced data. In order to solve this problem,
there are several solutions. One solution is the so called SMOTE which stands for *S**ynthetic **M**inority
**O**ver-Sampling **Te**chnique. For further information on how to implement this method in Python, please check the
following link

    *`How to Deal with Imbalanced Data using SMOTE ? <https://medium.com/analytics-vidhya/balance-your-data-using-smote-98e4d79fcddb>`__

Imputation strategies
----------------------
In order to deal with missing values, a more sophisticated imputation strategy can be used. For further information on
how to implement this method in Python, please check the following link

    *`Multivariate feature imputation <https://scikit-learn.org/stable/modules/impute.html#multivariate-feature-imputation>`__