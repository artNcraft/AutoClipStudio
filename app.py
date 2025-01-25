import gradio as gr
import os
from oauth_handler import OAuthHandler
from youtube_uploader import YouTubeUploader
from user_management import UserManager

# Initialize OAuth handler, YouTube uploader, and User manager
oauth_handler = OAuthHandler()
youtube_uploader = YouTubeUploader()
user_manager = UserManager()

def signup(userid, email):
    if user_manager.create_user(userid, email):
        return gr.update(visible=True), gr.update(visible=False), f"User {userid} created successfully!"
    else:
        return gr.update(visible=False), gr.update(visible=True), "User already exists or invalid input."

def login_with_google():
    auth_url = oauth_handler.get_authorization_url()
    return auth_url

def handle_oauth_callback(code):
    tokens = oauth_handler.exchange_code_for_tokens(code)
    if tokens:
        return gr.update(visible=True), "Authentication successful!"
    else:
        return gr.update(visible=False), "Authentication failed."

def upload_video(file, title, description, tags, privacy):
    video_id = youtube_uploader.upload_video(file.name, title, description, tags, privacy)
    if video_id:
        return f"Video uploaded successfully! Video ID: {video_id}"
    else:
        return "Video upload failed."

with gr.Blocks() as app:
    gr.Markdown("# AutoClip Studio")
    
    with gr.Tab("Signup"):
        userid_input = gr.Textbox(label="User ID")
        email_input = gr.Textbox(label="Email")
        signup_button = gr.Button("Sign Up")
        signup_message = gr.Textbox(label="Message", interactive=False)
        
    with gr.Tab("Login"):
        google_login_button = gr.Button("Login with Google")
        auth_url_output = gr.Textbox(label="Authorization URL", interactive=False)
        code_input = gr.Textbox(label="Enter the authorization code")
        submit_code_button = gr.Button("Submit Code")
        auth_message = gr.Textbox(label="Authentication Message", interactive=False)
    
    with gr.Tab("Upload Video", visible=False) as upload_tab:
        file_input = gr.File(label="Select Video File")
        title_input = gr.Textbox(label="Video Title")
        description_input = gr.Textbox(label="Video Description")
        tags_input = gr.Textbox(label="Tags (comma-separated)")
        privacy_input = gr.Dropdown(["public", "private", "unlisted"], label="Privacy Setting")
        upload_button = gr.Button("Upload Video")
        upload_message = gr.Textbox(label="Upload Message", interactive=False)
    
    signup_button.click(signup, inputs=[userid_input, email_input], outputs=[upload_tab, gr.Tab("Signup"), signup_message])
    google_login_button.click(login_with_google, outputs=auth_url_output)
    submit_code_button.click(handle_oauth_callback, inputs=code_input, outputs=[upload_tab, auth_message])
    upload_button.click(upload_video, inputs=[file_input, title_input, description_input, tags_input, privacy_input], outputs=upload_message)

if __name__ == "__main__":
    app.launch()
