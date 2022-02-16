# Java-related Tricks and Commands

## Creating a JAR file

The basic format of the command for creating a JAR file is:

```
jar cf jar-file-name input-files
```

The options and arguments used in this command are:
- The `c` option indicates that you want to *create* a JAR file.
- The `f` option indicates that you want the output to go to a *file* rather than to `stdout`.
- `jar-file-name` is the name that you want the resulting JAR file to have. You can use any filename for a JAR file. By convention, JAR filenames are given a `.jar` extension, though this is not required.
- The `input-files` argument is a space-separated list of one or more files that you want to include in your JAR file. This argument can contain the wildcard symbol. If any of the input files are directories, the contents of those directories are added to the JAR archive recursively.
- This command will also generate a default manifest file for the JAR archive.
- The metadata in the JAR file, such as the entry names, comments, and contents of the manifest, must be encoded in UTF8.

Several other options to the `cf` options of the basic command:
- `v`: produces verbose output on `stdout` whlie the JAR file is being built;
- `0`: indicates that you don't want the JAR file to be compressed;
- `M`: indicates that the default manifest file should not be produced;
- `m`: used to include manifest information from an existing manifest file;
  - The format for using this option is `jar cmf jar-file-name existing-manifest-file input-files`
  - The manifest must end with a new line or carriage return. The last line will not be parsed properly if it does not end with a new line or carriage return.
- `C` to change directories during execution of the command.

An example:

In directory `PropertyGraph/target/classes` (under the `class/` directory, there are `com/` and `application.properties`):

```
jar cvmf ../../src/META-INF/MANIFEST.MF test.jar com
```

Run the JAR application:

```
java -jar test.jar arguments_to_JAR
```
