import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
// import '../../../components/post_card.dart';
import '../view_model/home_view_model.dart';

class HomeView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Placeholder();
  }
}














/*

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../components/post_card.dart';
import '../view_model/home_view_model.dart';

class HomeView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade200,
      body: Consumer<PostViewModel>(
        builder: (context, postViewModel, child) {
          final hasPosts = postViewModel.posts.isNotEmpty;

          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (hasPosts)
                  Padding(
                    padding: const EdgeInsets.fromLTRB(14, 7, 0, 7),
                    child: Text(
                      'Recent Posts',
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                Expanded(
                  child: ListView.builder(
                    itemCount: postViewModel.posts.length,
                    itemBuilder: (context, index) {
                      final post = postViewModel.posts[index];
                      return PostCard(
                        content: post.content,
                        imageUrl: 'https://i.redd.it/n6fd1y3tbmb51.jpg',
                        username: 'John',
                        userProfileUrl: 'https://img.goodfon.com/wallpaper/big/0/48/paris-city-night-scenery-digital-art-4k.webp',
                        datePosted: '24-oct-2024', // Placeholder date
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

 */