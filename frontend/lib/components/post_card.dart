import 'package:flutter/material.dart';
import 'package:frontend/screens/comments_page/views/comments_view.dart';

class PostCard extends StatelessWidget {
  final String username;
  final String userProfileUrl;
  final String datePosted;
  final String content;
  final String imageUrl;
  final VoidCallback onMoreTapped;
  final VoidCallback onCommentIconTapped; // Add a callback for the comment icon tap

  const PostCard({
    super.key,
    required this.username,
    required this.userProfileUrl,
    required this.datePosted,
    required this.content,
    required this.imageUrl,
    required this.onMoreTapped,
    required this.onCommentIconTapped, // Add the callback to the constructor
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white,
      margin: EdgeInsets.all(8.0),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16.0),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                CircleAvatar(
                  backgroundImage: NetworkImage(userProfileUrl),
                  radius: 20,
                ),
                const SizedBox(width: 8.0),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        username,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16.0,
                        ),
                      ),
                      Text(
                        datePosted,
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 16.0,
                        ),
                      ),
                    ],
                  ),
                ),
                InkWell(
                  onTap: onMoreTapped,
                  child: Icon(Icons.more_horiz),
                ),
              ],
            ),
          ),
          ClipRRect(
            child: Image.network(
              imageUrl,
              height: 400,
              width: double.infinity,
              fit: BoxFit.cover,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 0.0),
                  child: Row(
                    children: [
                      Icon(Icons.favorite, color: Colors.red, size: 27,),
                      SizedBox(width: 2.0),
                      Text('199', style: TextStyle(fontSize: 15),),
                      SizedBox(width: 12.0),
                      InkWell(
                        onTap: onCommentIconTapped,
                        child: Image.asset(
                          'assets/images/comment_icon.png',
                          width: 24, // Adjust size if needed
                          height: 24, // Adjust size if needed
                        ),
                      ),
                      SizedBox(width: 3.0),
                      Text('10 comments', style: TextStyle(fontSize: 15),),
                      Spacer(),
                      Icon(Icons.share),
                      SizedBox(width: 4,),
                      Icon(Icons.bookmark_border, size: 30, color: Colors.grey.shade600,)
                    ],
                  ),
                ),
                SizedBox(height: 16.0),
                Text(
                  content,
                  style: TextStyle(
                    fontSize: 15.0,
                  ),
                ),
                SizedBox(height: 7.0),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
