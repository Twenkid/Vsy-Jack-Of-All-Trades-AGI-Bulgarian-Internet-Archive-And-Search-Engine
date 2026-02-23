#VSY tools ... notes
## Parsers, AST, Tree-Sitter, ... 

```
npx tree-sitter generate
npx tree-sitter parse grammar/p0.ml

npx tree-sitter parse grammar/p1.ml --debug
```

```
...
skip character:' '
  consume character:'/'
  consume character:'/'
  consume character:' '
  consume character:'B'
  consume character:'i'
  consume character:'t'
  consume character:'w'
  consume character:'i'
  consume character:'s'
  consume character:'e'
  consume character:'/'
  consume character:'B'
  consume character:'o'
  consume character:'o'
  consume character:'l'
  consume character:'e'
  consume character:'a'
  consume character:'n'
  consume character:' '
  consume character:'N'
  consume character:'O'
  consume character:'T'
  consume character:' '
  consume character:'t'
  consume character:'e'
  consume character:'s'
  consume character:'t'
lexed_lookahead sym:comment, size:40
shift_extra
process version:0, version_count:1, state:4, row:35, col:39
lex_internal state:7, row:35, column:39
  skip character:10
  skip character:' '
  skip character:' '

....

process version:0, version_count:1, state:29, row:40, col:1
lex_internal state:7, row:40, column:1
  skip character:10
lexed_lookahead sym:end, size:1
reduce sym:block, child_count:3
reduce sym:function_definition, child_count:7
reduce sym:source_file_repeat1, child_count:2
reduce sym:source_file, child_count:1

accept
done
```

(...)
```

(source_file [0, 0] - [41, 0]
  (comment [0, 0] - [0, 33])
  (const_declaration [1, 0] - [1, 26]
    (identifier [1, 6] - [1, 14])
    (type [1, 16] - [1, 19])
    (integer_literal [1, 22] - [1, 25]))
  (var_declaration [2, 0] - [2, 27]
    (identifier [2, 4] - [2, 17])
    (type [2, 19] - [2, 22])
    (integer_literal [2, 25] - [2, 26]))
  (struct_definition [4, 0] - [7, 1]
    (identifier [4, 7] - [4, 12])
    (struct_field [5, 4] - [5, 11]
      (identifier [5, 4] - [5, 5])
      (type [5, 7] - [5, 10]))
    (struct_field [6, 4] - [6, 11]
      (identifier [6, 4] - [6, 5])
      (type [6, 7] - [6, 10])))
  (struct_definition [9, 0] - [13, 1]
    (identifier [9, 7] - [9, 13])
    (struct_field [10, 4] - [10, 15]
      (identifier [10, 4] - [10, 7])
      (type [10, 9] - [10, 14]
        (type_name [10, 9] - [10, 14])))
    (struct_field [11, 4] - [11, 12]
      (identifier [11, 4] - [11, 6])
      (type [11, 8] - [11, 11]))
    (struct_field [12, 4] - [12, 20]
      (identifier [12, 4] - [12, 13])
      (type [12, 15] - [12, 19])))
  (function_definition [15, 0] - [21, 1]
    (identifier [15, 3] - [15, 21])
    (parameter_list [15, 22] - [15, 42]
      (parameter [15, 22] - [15, 31]
        (identifier [15, 22] - [15, 24])
        (type [15, 26] - [15, 31]
          (type_name [15, 26] - [15, 31])))
      (parameter [15, 33] - [15, 42]
        (identifier [15, 33] - [15, 35])
        (type [15, 37] - [15, 42]
          (type_name [15, 37] - [15, 42]))))
    (type [15, 47] - [15, 50])
    (block [15, 51] - [21, 1]
      (var_declaration [16, 4] - [16, 30]
        (identifier [16, 8] - [16, 10])
        (type [16, 12] - [16, 15])
        (binary_expression [16, 18] - [16, 29]
          left: (field_access [16, 18] - [16, 22]
            (identifier [16, 18] - [16, 20])
            (identifier [16, 21] - [16, 22]))
          right: (field_access [16, 25] - [16, 29]
            (identifier [16, 25] - [16, 27])
            (identifier [16, 28] - [16, 29]))))
      (var_declaration [17, 4] - [17, 30]
        (identifier [17, 8] - [17, 10])
        (type [17, 12] - [17, 15])
        (binary_expression [17, 18] - [17, 29]
          left: (field_access [17, 18] - [17, 22]
            (identifier [17, 18] - [17, 20])
            (identifier [17, 21] - [17, 22]))
          right: (field_access [17, 25] - [17, 29]
            (identifier [17, 25] - [17, 27])
            (identifier [17, 28] - [17, 29]))))
      (comment [19, 4] - [19, 43])
      (return_statement [20, 4] - [20, 29]
        (binary_expression [20, 11] - [20, 28]
          left: (binary_expression [20, 11] - [20, 18]
            left: (identifier [20, 11] - [20, 13])
            right: (identifier [20, 16] - [20, 18]))
          right: (binary_expression [20, 21] - [20, 28]
            left: (identifier [20, 21] - [20, 23])
            right: (identifier [20, 26] - [20, 28]))))))
  (function_definition [23, 0] - [40, 1]
    (identifier [23, 3] - [23, 7])
    (type [23, 13] - [23, 17])
    (block [23, 18] - [40, 1]
      (var_declaration [24, 4] - [28, 6]
        (identifier [24, 8] - [24, 15])
        (type [24, 17] - [24, 23]
          (type_name [24, 17] - [24, 23]))
        (struct_literal [24, 26] - [28, 5]
          (identifier [24, 26] - [24, 32])
          (field_init_list [25, 8] - [27, 24]
            (field_init [25, 8] - [25, 35]
              (identifier [25, 8] - [25, 11])
              (struct_literal [25, 13] - [25, 35]
                (identifier [25, 13] - [25, 18])
                (field_init_list [25, 21] - [25, 33]
                  (field_init [25, 21] - [25, 26]
                    (identifier [25, 21] - [25, 22])
                    (integer_literal [25, 24] - [25, 26]))
                  (field_init [25, 28] - [25, 33]
                    (identifier [25, 28] - [25, 29])
                    (integer_literal [25, 31] - [25, 33])))))
            (field_init [26, 8] - [26, 13]
              (identifier [26, 8] - [26, 10])
              (integer_literal [26, 12] - [26, 13]))
            (field_init [27, 8] - [27, 23]
              (identifier [27, 8] - [27, 17])
              (identifier [27, 19] - [27, 23])))))
      (var_declaration [30, 4] - [30, 19]
        (identifier [30, 8] - [30, 9])
        (type [30, 11] - [30, 14])
        (integer_literal [30, 17] - [30, 18]))
      (while_statement [31, 4] - [39, 5]
        (binary_expression [31, 11] - [31, 23]
          left: (identifier [31, 11] - [31, 12])
          right: (identifier [31, 15] - [31, 23]))
        (block [31, 25] - [39, 5]
          (if_statement [32, 8] - [37, 9]
            (binary_expression [32, 12] - [32, 22]
              left: (binary_expression [32, 12] - [32, 17]
                left: (identifier [32, 12] - [32, 13])
                right: (integer_literal [32, 16] - [32, 17]))
              right: (integer_literal [32, 21] - [32, 22]))
            (block [32, 24] - [34, 9]
              (assignment_statement [33, 12] - [33, 46]
                (lvalue [33, 12] - [33, 25]
                  (identifier [33, 12] - [33, 25]))
                (binary_expression [33, 28] - [33, 45]
                  left: (identifier [33, 28] - [33, 41])
                  right: (integer_literal [33, 44] - [33, 45]))))
            (block [34, 15] - [37, 9]
              (comment [35, 12] - [35, 39])
              (var_declaration [36, 12] - [36, 36]
                (identifier [36, 16] - [36, 20])
                (type [36, 22] - [36, 26])
                (unary_expression [36, 29] - [36, 35]
                  (identifier [36, 30] - [36, 35])))))
          (assignment_statement [38, 8] - [38, 18]
            (lvalue [38, 8] - [38, 9]
              (identifier [38, 8] - [38, 9]))
            (binary_expression [38, 12] - [38, 17]
              left: (identifier [38, 12] - [38, 13])
              right: (integer_literal [38, 16] - [38, 17]))))))))

```



