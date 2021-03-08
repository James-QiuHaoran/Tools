## jq

jq is a lightweight and flexible command-line JSON processor.
jq is like sed for JSON data - you can use it to slice and filter and map and transform structured data with the same ease that sed, awk, grep and friends let you play with text.

### Tutorial

https://stedolan.github.io/jq/tutorial/

### Examples

Parse JSON data using `jq`:
- Get all keys: `jq keys file_name.json`
- Get the data associated with a key: `jq .data file_name.json`
- Get the list of the data: `jq ".data | .[]" file_name.json`
- Get the first item of the list: `jq ".data | .[0]" file_name.json`
