from core.lex import run

code = """
<?php //php 7.2.24
    $num1=10;
    $num2=20;
    IF ($num1>$num2) {
        $bignum = $num1;
        PRINT "Big Number is " . $bignum;
    }
    ELSE {
        $bignum = $num2;
        PRINT "Big Number is " . $bignum;
    }
?>
"""

run(code)
