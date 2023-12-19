mod app;
mod node;
mod security;
mod ui;
use app::{App, CurrentScreen, Mode};
use crossterm::event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode, KeyModifiers};
use crossterm::execute;
use crossterm::terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen};
use ratatui::backend::Backend;
use ratatui::prelude::CrosstermBackend;
use ratatui::Terminal;
use std::cmp::Ordering;
use std::net::ToSocketAddrs;
use ui::ui;

type ExitResult = std::io::Result<bool>;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // setup terminal
    enable_raw_mode()?;
    execute!(std::io::stdout(), EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(std::io::stdout());
    let mut terminal = Terminal::new(backend)?;
    let mut app = App::new();
    let exit_result = run_app(&mut terminal, &mut app);

    // restore terminal
    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen, DisableMouseCapture)?;
    terminal.show_cursor()?;
    match exit_result {
        Ok(_) => {}
        Err(err) => {
            eprintln!("{err:?}");
        }
    }
    Ok(())
}

fn run_app<B: Backend>(terminal: &mut Terminal<B>, app: &mut App) -> ExitResult {
    // start grpc server

    // running
    loop {
        terminal.draw(|f| ui(f, app))?;
        if let Event::Key(key) = event::read()? {
            if key.code == KeyCode::Char('c') && key.modifiers == KeyModifiers::CONTROL {
                return ExitResult::Ok(true);
            };
            match app.current_screen {
                CurrentScreen::Main => {
                    // main page
                    match key.code {
                        KeyCode::Char('r') | KeyCode::Char('R') => {
                            app.current_screen = CurrentScreen::Register;
                            app.mode = Mode::InputUsername;
                            app.input_buffer = app::InputBuffer::default();
                        }
                        KeyCode::Char('l') | KeyCode::Char('L') => {
                            app.current_screen = CurrentScreen::Login;
                            app.mode = Mode::InputUsername;
                            app.input_buffer = app::InputBuffer::default();
                        }
                        _ => {}
                    }
                }
                CurrentScreen::Login => {
                    // login page
                    app.notice = String::from("Clear!");
                    match app.mode {
                        Mode::InputUsername => match key.code {
                            KeyCode::Char(c) => {
                                app.input_buffer.username.push(c);
                            }
                            KeyCode::Backspace | KeyCode::Delete => {
                                app.input_buffer.username.pop();
                            }
                            KeyCode::Down => app.mode = Mode::InputPassword,
                            KeyCode::Up => app.notice = String::from("Already at the top!"),
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        Mode::InputPassword => match key.code {
                            KeyCode::Char(c) => {
                                app.input_buffer.password.push(c);
                            }
                            KeyCode::Backspace | KeyCode::Delete => {
                                app.input_buffer.password.pop();
                            }
                            KeyCode::Up => app.mode = Mode::InputUsername,
                            KeyCode::Down => app.mode = Mode::LoginButton,
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        Mode::LoginButton => match key.code {
                            KeyCode::Enter => {
                                let username = app.input_buffer.username.clone();
                                let password = app.input_buffer.password.clone();
                                if username.is_empty() {
                                    app.notice = String::from("Username cannot be empty!");
                                    continue;
                                }
                                if password.is_empty() {
                                    app.notice = String::from("Password cannot be empty!");
                                    continue;
                                }
                                app.notice = String::from("Verifying...")
                            }
                            KeyCode::Up => app.mode = Mode::InputPassword,
                            KeyCode::Down => app.notice = String::from("Already at the bottom!"),
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        _ => {}
                    }
                }
                CurrentScreen::Register => {
                    // register page
                    app.notice = String::from("Clear!");
                    match app.mode {
                        Mode::InputUsername => match key.code {
                            KeyCode::Char(c) => {
                                app.input_buffer.username.push(c);
                            }
                            KeyCode::Backspace | KeyCode::Delete => {
                                app.input_buffer.username.pop();
                            }
                            KeyCode::Down => app.mode = Mode::InputEmail,
                            KeyCode::Up => app.notice = String::from("Already at the top!"),
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        Mode::InputEmail => match key.code {
                            KeyCode::Char(c) => {
                                app.input_buffer.email.push(c);
                            }
                            KeyCode::Backspace | KeyCode::Delete => {
                                app.input_buffer.email.pop();
                            }
                            KeyCode::Up => app.mode = Mode::InputUsername,
                            KeyCode::Down => app.mode = Mode::InputPassword,
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        Mode::InputPassword => match key.code {
                            KeyCode::Char(c) => {
                                app.input_buffer.password.push(c);
                            }
                            KeyCode::Backspace | KeyCode::Delete => {
                                app.input_buffer.password.pop();
                            }
                            KeyCode::Up => app.mode = Mode::InputEmail,
                            KeyCode::Down => app.mode = Mode::InputPasswordConfirm,
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        Mode::InputPasswordConfirm => match key.code {
                            KeyCode::Char(c) => {
                                app.input_buffer.password_confirm.push(c);
                            }
                            KeyCode::Backspace | KeyCode::Delete => {
                                app.input_buffer.password_confirm.pop();
                            }
                            KeyCode::Up => app.mode = Mode::InputPassword,
                            KeyCode::Down => app.mode = Mode::RegisterButton,
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        Mode::RegisterButton => match key.code {
                            KeyCode::Enter => {
                                let username = app.input_buffer.username.clone();
                                let password = app.input_buffer.password.clone();
                                let password_confirm = app.input_buffer.password_confirm.clone();
                                let email = app.input_buffer.email.clone();
                                if username.is_empty() {
                                    app.notice = String::from("Username cannot be empty!");
                                    continue;
                                }
                                if email.is_empty() {
                                    app.notice = String::from("Email cannot be empty!");
                                    continue;
                                }
                                if password.is_empty() {
                                    app.notice = String::from("Password cannot be empty!");
                                    continue;
                                }
                                if password.cmp(&password_confirm) != Ordering::Equal {
                                    app.notice = String::from("Passwords umatch!");
                                    continue;
                                }
                                app.notice = String::from("Communicating...")
                            }
                            KeyCode::Up => app.mode = Mode::InputPassword,
                            KeyCode::Down => app.notice = String::from("Already at the bottom!"),
                            _ => app.notice = format!("Invalid Key '{:?}'", key.code),
                        },
                        _ => {}
                    }
                }
                CurrentScreen::Chat => {
                    // chat page
                }
            }
        }
    }
    Ok(true)
}
