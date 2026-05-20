package com.jfranco.practice.exercises;

public class Exercise01Basics {

    public boolean isEven(int number) {
        return number % 2 == 0;
    }

    public int sum(int left, int right) {
        return left + right;
    }

    public String reverse(String value) {
        if (value == null) {
            throw new IllegalArgumentException("value cannot be null");
        }

        return new StringBuilder(value).reverse().toString();
    }
}
