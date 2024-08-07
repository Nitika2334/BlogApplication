import 'package:flutter/material.dart';

class GenTextField extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final bool obscureText;

  const GenTextField({
    super.key,
    required this.controller,
    required this.hintText,
    required this.obscureText,
  });

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      obscureText: obscureText,
      decoration: InputDecoration(
        hintText: hintText,
        border: InputBorder.none,
        fillColor: Colors.grey.shade200,
        hintStyle: TextStyle(color: Colors.grey[500], fontSize: 19),
      ),
    );

  }
}
