# TODO List for Implementing Features

## Feature 1: Make Email Optional in Signup
- Modify `confessions/forms.py` to make email field not required in SignUpForm.
- Commit: "Make email optional in signup form for anonymous users"

## Feature 2: Display u/user Above Confessions and Comments
- Update `confessions/templates/confessions/confession_list.html` to show "u/{{ author.username }}" or "Anonymous" above each confession.
- Update the same template to show "u/{{ comment.author.username }}" or "Anonymous" for each comment.
- Commit: "Add u/user display above confessions and comments"

## Feature 3: Change Comment Button to Icon with Count
- Update `confessions/templates/confessions/confession_list.html` to replace "Comment" button with icon and comment count beside it.
- Ensure it still toggles the comments section.
- Commit: "Replace comment button with icon and comment count"

## Feature 4: Allow Anonymous Confession Posting
- Add a form in `confessions/templates/confessions/confession_list.html` for posting confessions without login (anonymous).
- Update `confessions/views.py` to handle anonymous confession posting in confession_list view.
- Commit: "Add anonymous confession posting option"

## Testing and Cleanup
- Test all changes locally.
- Ensure no sensitive API keys are committed (check .gitignore includes .env).
- Commit: "Update .gitignore to include .env if not already"

## Fix Gemini API Configuration
- Install python-dotenv for environment variable management.
- Create .env file with GEMINI_API_KEY placeholder.
- Update confizz/settings.py to load .env file.
- Add GEMINI_API_KEY to settings.py.
- Update confessions/views.py and confizz/confessions/views.py to use settings.GEMINI_API_KEY instead of os.environ.get.
- Test the summarize_comments endpoint after setting the API key.
