from google.adk.tools.tool_context import ToolContext

def exit_conversation(tool_context: ToolContext):
    """
    Simple tool that simply implies intent for the user to finish the conversation. 
    Sets flag in ToolContext.state for key "user_wishes_to_exit" to True

    Args: 
        context (ToolContext): Session state 

    Returns:
        None
    """
    tool_context.state["user_wishes_to_exit"] = True