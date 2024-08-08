import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../view_model/comments_view_model.dart';
import 'package:timeago/timeago.dart' as timeago;

class CommentsBottomSheet extends StatelessWidget {
  const CommentsBottomSheet({super.key});

  @override
  Widget build(BuildContext context) {
    final viewModel = Provider.of<CommentsViewModel>(context);
    final TextEditingController _controller = TextEditingController();

    return LayoutBuilder(
      builder: (context, constraints) {
        final keyboardVisible = MediaQuery.of(context).viewInsets.bottom > 0;

        return Container(
          padding: EdgeInsets.fromLTRB(
            20.0,
            20.0,
            20.0,
            keyboardVisible ? MediaQuery.of(context).viewInsets.bottom : 20.0,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Align(
                alignment: Alignment.centerLeft,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Comments',
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    IconButton(
                      icon: Icon(Icons.close),
                      onPressed: () {
                        Navigator.of(context).pop(); // Close the bottom sheet
                      },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 8.0),
              Divider(thickness: 1.0, color: Colors.grey.shade400), // Horizontal line
              const SizedBox(height: 8.0),
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      ...viewModel.comments.map(
                            (comment) => ListTile(
                          leading: CircleAvatar(
                            backgroundImage: NetworkImage('https://images7.alphacoders.com/854/thumb-350-854878.jpg'),
                            radius: 20,
                          ),
                          title: Row(
                            children: [
                              Text(
                                comment.author,
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                              SizedBox(width: 8.0), // Space between name and date
                              Text(
                                timeago.format(comment.timestamp, locale: 'en_short'),
                                style: TextStyle(color: Colors.grey),
                              ),
                            ],
                          ),
                          subtitle: Text(comment.text),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Row(
                  children: [
                    CircleAvatar(
                      backgroundImage: NetworkImage('https://images7.alphacoders.com/854/thumb-350-854878.jpg'),
                      radius: 16,
                    ),
                    const SizedBox(width: 8.0),
                    Expanded(
                      child: TextField(
                        controller: _controller,
                        onSubmitted: (text) {
                          if (text.trim().isNotEmpty) {
                            viewModel.addComment('You', text);
                            _controller.clear();
                            FocusScope.of(context).unfocus();
                          }
                        },
                        decoration: InputDecoration(
                          hintText: 'Add a comment...',
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(50.0),
                            borderSide: BorderSide(color: Colors.grey.shade300),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(20.0),
                            borderSide: BorderSide(color: Colors.blue),
                          ),
                          suffixIcon: IconButton(
                            icon: Icon(Icons.send, color: Colors.blue),
                            onPressed: () {
                              if (_controller.text.trim().isNotEmpty) {
                                viewModel.addComment('You', _controller.text);
                                _controller.clear();
                                FocusScope.of(context).unfocus(); // Close the keyboard
                              }
                            },
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
