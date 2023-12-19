pub enum CurrentScreen {
    Main,
    Login,
    Register,
    Chat,
}

#[derive(PartialEq)]
pub enum Mode {
    Normal,
    InputUsername,
    InputPassword,
    InputPasswordConfirm,
    InputEmail,
    LoginButton,
    RegisterButton,
}

pub struct User {
    pub username: String,
    pub email: String,
}

#[derive(PartialEq, Default)]
pub struct InputBuffer {
    pub username: String,
    pub password: String,
    pub password_confirm: String,
    pub email: String,
    pub message: String,
}

pub struct App {
    pub current_screen: CurrentScreen,
    pub mode: Mode,
    pub user: User,
    pub input_buffer: InputBuffer,
    pub notice: String,
    pub logged: bool,
}

impl App {
    pub fn new() -> App {
        App {
            current_screen: CurrentScreen::Main,
            mode: Mode::Normal,
            user: User {
                username: String::from(""),
                email: String::from(""),
            },
            input_buffer: InputBuffer::default(),
            notice: String::from(""),
            logged: false,
        }
    }
}
