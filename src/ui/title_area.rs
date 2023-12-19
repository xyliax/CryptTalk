use crate::app::App;
use ratatui::{
    layout::{Alignment, Rect},
    style::Stylize,
    widgets::{block::Title, Block, BorderType, Borders, Paragraph},
    Frame,
};

pub fn ui(f: &mut Frame, _app: &App, title_chunk: &Rect) {
    let title_block = Block::default()
        .title(Title::from("CryptTalk").alignment(Alignment::Center))
        .title(Title::from("Press ESC to Home".red().underlined()).alignment(Alignment::Right))
        .borders(Borders::ALL)
        .border_type(BorderType::Rounded)
        .blue()
        .bold();
    let title = Paragraph::new("COMP4334 ETE Online Chat - Team 11".green())
        .block(title_block)
        .alignment(Alignment::Center);
    f.render_widget(title, *title_chunk);
}
