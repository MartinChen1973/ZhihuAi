from semantic_kernel.skill_definition import sk_function

class NormalCommandVerifier:
    def verify(self, command: str) -> str:
        leggal_commands = ["ls", "cat", "head", "tail", "echo", "dir", "cd", "md", "copy"]
        for leggal_command in leggal_commands:
            if command.startswith(f"{leggal_command} "):
                print(f"{command} starts with {leggal_command}, so it's leggal.")
                return "合法"
        return "非法"

class NativeCommandVerifier:
    @sk_function(
        name="verifyCommand",
        description="检查Dos、Windows和Linux命令是否安全合法",
    )
    def verify(self, command: str) -> str:
        leggal_commands = ["ls", "cat", "head", "tail", "echo", "dir", "cd", "md", "copy"]
        for leggal_command in leggal_commands:
            if command == leggal_command or command.startswith(f"{leggal_command} "):
                print(f"{command} starts with {leggal_command}, so it's leggal.")
                return f"指令为：{command}，此指令【合法】"
        return f"指令为：{command}，此指令【非法】"
