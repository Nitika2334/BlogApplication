import 'package:flutter/material.dart';
import 'package:frontend/screens/delete_drawer/views/delete_view.dart';
import 'package:frontend/screens/functionality_drawer/views/functionality_view.dart';
import 'package:provider/provider.dart';
import '../../../components/post_card.dart';
import '../../comments_page/views/comments_view.dart';
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
                        username: 'John Doe',
                        userProfileUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMlresTFqYp-__qOdruWQkL6Xxyd0Fm1cj2Q&s',
                        datePosted: 'August 7, 2024',
                        content: 'This is a sample post content.',
                        imageUrl: 'https://c4.wallpaperflare.com/wallpaper/44/145/123/starry-night-sky-night-starry-night-wallpaper-preview.jpg',
                        onCommentIconTapped: () {
                          showModalBottomSheet(
                            context: context,
                            builder: (context) => CommentsBottomSheet(),
                          );
                        },
                        onMoreTapped: () {
                          showModalBottomSheet(
                            context: context,
                            builder: (context) => FunctionalityView(
                              onDeletePost: () {
                                showModalBottomSheet(
                                  context: context,
                                  builder: (context) => DeleteView(),
                                );
                              },
                            ),
                          );
                        },
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
