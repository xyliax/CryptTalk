use futures::stream::StreamExt;
use libp2p::{
    mdns, noise,
    swarm::{NetworkBehaviour, SwarmEvent},
    tcp, yamux, Multiaddr, PeerId, SwarmBuilder,
};
use std::error::Error;
use tokio::select;

// We create a custom network behaviour that includes Mdns.
#[derive(NetworkBehaviour)]
struct MyBehaviour {
    mdns: mdns::tokio::Behaviour,
}

async fn find_peer() -> Result<(), Box<dyn Error>> {
    let local_key = libp2p::identity::Keypair::generate_ed25519();
    let local_peer_id = PeerId::from(local_key.public());

    let tcp_config = tcp::Config::new();

    let behaviour = MyBehaviour {
        mdns: mdns::tokio::Behaviour::new(mdns::Config::default(), local_peer_id.clone())?,
    };

    let mut swarm = libp2p::SwarmBuilder::with_new_identity()
        .with_tokio()
        .with_tcp(tcp::Config::default(), noise::Config::new, yamux::Config::default)?
        .with_behaviour(|key| {
            let mdns = mdns::tokio::Behaviour::new(mdns::Config::default(), key.public().to_peer_id())?;
            Ok(MyBehaviour { mdns })
        })?
        .build();

    let listen_addr: Multiaddr = format!("/ip4/0.0.0.0/tcp/0").parse()?;
    swarm.listen_on(listen_addr)?;
    
    // Kick it off
    loop {
        select! {
            event = swarm.select_next_some() => match event {
                SwarmEvent::Behaviour(MyBehaviourEvent::Mdns(mdns::Event::Discovered(peers))) => {
                    handle_discovered_peers(peers);
                },
                _ => {}
            }
        }
    }
}

fn handle_discovered_peers(peers: Vec<(PeerId, Multiaddr)>) {
    for (peer_id, _) in peers {
        println!("mDNS discovered a new peer: {:?}", peer_id);
    }
}

fn handle_expired_peers(expired: Vec<(PeerId, Multiaddr)>) {
    for (peer_id, _) in expired {
        println!("mDNS discovered peer has expired: {:?}", peer_id);
    }
}
