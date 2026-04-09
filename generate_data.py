import pandas as pd
import os

os.makedirs('datasets', exist_ok=True)

# Massive Database with 50 Movies
movies = {
    'id': list(range(1, 51)),
    'title':[
        # Original 26
        'Interstellar', '3 Idiots', 'Avengers: Endgame', 'Dangal', 'The Dark Knight', 
        'Zindagi Na Milegi Dobara', 'Inception', 'Pathaan', 'Dune', 'Spider-Man', 
        'Sholay', 'Avatar', 'Jawan', 'The Matrix', 'KGF: Chapter 2', 
        'Bahubali 2', 'Joker', 'Titanic', 'Yeh Jawaani Hai Deewani', 'RRR',
        'Oppenheimer', 'PK', 'Jurassic Park', 'Chennai Express', 'Gladiator', 'Gravity',
        # 24 NEW ADDITIONS
        'John Wick', 'Animal', 'Pushpa: The Rise', 'Kantara', 'Bajrangi Bhaijaan',
        'Drishyam', 'Lagaan', 'Swades', 'Munna Bhai M.B.B.S.', 'Andhadhun',
        'Deadpool', 'The Hangover', 'The Martian', 'Blade Runner 2049', 'Star Wars: A New Hope',
        'Back to the Future', 'Iron Man', 'Guardians of the Galaxy', 'Mad Max: Fury Road', 'The Terminator',
        'Spider-Man: No Way Home', 'Kalki 2898 AD', 'Salaar', 'Sanju'
    ],
    'language':[
        'English', 'Hindi', 'English', 'Hindi', 'English', 'Hindi', 'English', 'Hindi', 'English', 'English', 
        'Hindi', 'English', 'Hindi', 'English', 'Hindi/Kannada', 'Hindi/Telugu', 'English', 'English', 'Hindi', 'Hindi/Telugu',
        'English', 'Hindi', 'English', 'Hindi', 'English', 'English',
        # New Additions
        'English', 'Hindi', 'Telugu/Hindi', 'Kannada/Hindi', 'Hindi',
        'Hindi', 'Hindi', 'Hindi', 'Hindi', 'Hindi',
        'English', 'English', 'English', 'English', 'English',
        'English', 'English', 'English', 'English', 'English',
        'English', 'Telugu/Hindi', 'Telugu/Hindi', 'Hindi'
    ],
    'genres':[
        'Sci-Fi Drama', 'Comedy Drama', 'Action Sci-Fi', 'Sports Drama', 'Action Crime', 
        'Adventure Comedy', 'Sci-Fi Thriller', 'Action Thriller', 'Sci-Fi Adventure', 'Action Adventure', 
        'Action Adventure', 'Sci-Fi Action', 'Action Thriller', 'Sci-Fi Action', 'Action Drama', 
        'Action Fantasy', 'Crime Drama', 'Romance Drama', 'Romance Comedy', 'Action Historical',
        'Biography Drama', 'Comedy Sci-Fi', 'Sci-Fi Adventure', 'Action Comedy', 'Action Drama', 'Sci-Fi Thriller',
        # New Additions
        'Action Thriller', 'Action Drama', 'Action Drama', 'Action Thriller', 'Comedy Drama',
        'Crime Thriller', 'Sports Drama', 'Drama', 'Comedy', 'Crime Thriller Comedy',
        'Action Comedy', 'Comedy', 'Sci-Fi Adventure', 'Sci-Fi Thriller', 'Sci-Fi Adventure',
        'Sci-Fi Comedy', 'Action Sci-Fi', 'Action Comedy Sci-Fi', 'Action Sci-Fi', 'Action Sci-Fi',
        'Action Adventure', 'Action Sci-Fi', 'Action Thriller', 'Biography Drama'
    ],
    'description':[
        # Original 26
        'Explorers travel through a wormhole to save humanity from dying Earth.', 
        'Three engineering students learn about life, friendship, and success.', 
        'The Avengers assemble once more to reverse Thanos destroying the universe.', 
        'A former wrestler trains his two daughters to win gold medals for India.', 
        'Batman faces the psychological threat of the Joker in Gotham city.', 
        'Three friends take a bachelor trip to Spain and discover themselves.', 
        'A thief steals secrets through dream-sharing technology and inception.', 
        'An Indian spy takes on a ruthless mercenary over a deadly virus.',
        'A noble family becomes embroiled in a war for control of a desert planet.', 
        'A teenager gains spider-like abilities and fights evil.',
        'Two ex-convicts are hired to capture a ruthless bandit in a village.', 
        'A marine on an alien planet gets torn between two worlds and species.',
        'A man driven by a personal vendetta to rectify the wrongs in society.', 
        'A computer hacker learns the true nature of reality and fights machines.',
        'An assassin fights enemies to retain control over a gold mine.',
        'A son learns about his fathers legendary past and battles his evil uncle.',
        'A mentally troubled comedian embarks on a downward spiral of crime.',
        'A romance unfolds on the ill-fated sinking ship.',
        'Friends reunite at a wedding and explore love and life goals.',
        'Two legendary revolutionaries fight against the British colonial rule.',
        'The story of the scientist who helped develop the atomic bomb.',
        'An alien stranded on Earth asks questions about religion and humanity.',
        'Dinosaurs break loose in a theme park and hunt humans.',
        'A man takes his grandfathers ashes to Rameswaram and meets a mafia daughter.',
        'A Roman general is betrayed and forced to become a gladiator.',
        'Two astronauts are stranded in deep space after their shuttle is destroyed.',
        # New 24
        'An ex-hitman comes out of retirement to track down the gangsters that wronged him.',
        'A sons love for his father turns into a dark obsession for vengeance.',
        'A laborer rises through the ranks of a red sandalwood smuggling syndicate.',
        'A fiery young man clashes with an upright forest officer in a mystical village.',
        'An Indian man takes on the task of taking a mute Pakistani girl back to her homeland.',
        'A desperate man takes extreme measures to save his family from the dark side of the law.',
        'Villagers in Victorian India stake their future on a game of cricket against their British rulers.',
        'A successful Indian scientist returns to his village and finds his true calling.',
        'A local goon goes to medical school to fulfill his fathers dream.',
        'A blind pianist gets entangled in a series of shocking murders.',
        'A wisecracking mercenary gets experimented on and seeks revenge.',
        'Three buddies wake up from a bachelor party in Vegas with no memory of the previous night.',
        'An astronaut becomes stranded on Mars and must survive until a rescue mission arrives.',
        'A young blade runner discovers a long-buried secret that could plunge society into chaos.',
        'Luke Skywalker joins forces with a Jedi Knight to save the galaxy from the Empires world-destroying battle station.',
        'A teenager is accidentally sent 30 years into the past in a time-traveling DeLorean.',
        'A billionaire engineer builds a high-tech suit of armor to fight evil.',
        'A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.',
        'In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland.',
        'A cyborg is sent from the future on a deadly mission to kill Sarah Connor.',
        'Spider-Man seeks the help of Doctor Strange to forget his exposed secret identity, with dangerous consequences.',
        'A modern avatar of Vishnu descends on Earth to protect humanity from dark forces.',
        'A gang leader makes a promise to a dying friend to protect his kingdom.',
        'The controversial and colorful life of Bollywood actor Sanjay Dutt.'
    ],
    'mood':[
        'Thoughtful', 'Happy', 'Thrilled', 'Motivated', 'Thrilled', 'Happy', 'Thoughtful', 'Thrilled', 'Thoughtful', 'Happy', 
        'Thrilled', 'Thoughtful', 'Thrilled', 'Thoughtful', 'Thrilled', 'Motivated', 'Thoughtful', 'Thoughtful', 'Happy', 'Motivated',
        'Thoughtful', 'Happy', 'Thrilled', 'Happy', 'Motivated', 'Thrilled',
        # New Additions
        'Thrilled', 'Thrilled', 'Motivated', 'Thrilled', 'Happy',
        'Thoughtful', 'Motivated', 'Thoughtful', 'Happy', 'Thrilled',
        'Happy', 'Happy', 'Motivated', 'Thoughtful', 'Motivated',
        'Happy', 'Motivated', 'Happy', 'Thrilled', 'Thrilled',
        'Thrilled', 'Thrilled', 'Thrilled', 'Motivated'
    ],
    'rating':[
        4.8, 4.9, 4.7, 4.8, 4.9, 4.8, 4.8, 4.3, 4.6, 4.5, 
        4.9, 4.7, 4.5, 4.8, 4.7, 4.8, 4.6, 4.7, 4.6, 4.8,
        4.9, 4.8, 4.7, 4.2, 4.8, 4.5,
        # New Additions
        4.7, 4.2, 4.6, 4.8, 4.8,
        4.7, 4.8, 4.8, 4.8, 4.8,
        4.6, 4.5, 4.7, 4.6, 4.7,
        4.8, 4.7, 4.7, 4.8, 4.7,
        4.8, 4.5, 4.4, 4.6
    ],
    'poster':[
        # Using a mix of TMDB links. Remember, your frontend 'onerror' tag will auto-generate beautiful covers if any of these are blocked!
        'https://image.tmdb.org/t/p/w500/gEU2QlsEOWpNATsc9pbD054rKwi.jpg', 'https://image.tmdb.org/t/p/w500/66A904EDSRbbNEbAEEb0W29UWA3.jpg',
        'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg', 'https://image.tmdb.org/t/p/w500/w2iA9LHeXxa1I2DOUgAALsOSmta.jpg',
        'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg', 'https://image.tmdb.org/t/p/w500/3AhtZ48s3y0j7N20wL3a20yW6uM.jpg',
        'https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg', 'https://image.tmdb.org/t/p/w500/n1OD0ZkOeaZf7BAlRzP9B54ZqJb.jpg',
        'https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg', 'https://image.tmdb.org/t/p/w500/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg',
        'https://image.tmdb.org/t/p/w500/uU0wQ7v7sJ0L2s4yv2T1F14Z4wY.jpg', 'https://image.tmdb.org/t/p/w500/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg',
        'https://image.tmdb.org/t/p/w500/jILeVcEKspA11S1f4oGhgAUBzQf.jpg', 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GvwJwB02xcI0.jpg',
        'https://image.tmdb.org/t/p/w500/b1DEFm8XgP5R8ZExegE1mD0XU44.jpg', 'https://image.tmdb.org/t/p/w500/x2BhwT8i5VqO6WwK43sA0eOIKG2.jpg',
        'https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg', 'https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg',
        'https://image.tmdb.org/t/p/w500/51m8IeA98ZfP9Pj0FItq8Iu2A4i.jpg', 'https://image.tmdb.org/t/p/w500/nEufeZlyAOLqO2brrs0yeO1WMe6.jpg',
        'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg', 'https://image.tmdb.org/t/p/w500/z0tT6E6a4t9E0f7p4uR7F1871aG.jpg',
        'https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg', 'https://image.tmdb.org/t/p/w500/uYZbTWe0j2g8r2mS5o1lV1AomM3.jpg',
        'https://image.tmdb.org/t/p/w500/ty8TGRuvEU1HkU4574I7zL8Z785.jpg', 'https://image.tmdb.org/t/p/w500/9vD0aXAE9z1L0r3O8Nsh9GAYl1k.jpg',
        # 24 New Additions
        'https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg', 'https://image.tmdb.org/t/p/w500/rKFVw9fC05Z40xQxG9hK6w1e7Jj.jpg',
        'https://image.tmdb.org/t/p/w500/r1yABxEAANL2R1oE9q0q56x7LgA.jpg', 'https://image.tmdb.org/t/p/w500/bBhwX0B6T85U1l9Y9z9jR6P7V9Q.jpg',
        'https://image.tmdb.org/t/p/w500/w1TijDqX9kX7Z3zYq0e1k3tZ9U4.jpg', 'https://image.tmdb.org/t/p/w500/x5z5b0q6l3b6b6z7y5b5b5b5b5b.jpg',
        'https://image.tmdb.org/t/p/w500/2L2z0z9y1b7b7b7b7b7b7b7b7b7.jpg', 'https://image.tmdb.org/t/p/w500/3L3z0z9y1b7b7b7b7b7b7b7b7b7.jpg',
        'https://image.tmdb.org/t/p/w500/4L4z0z9y1b7b7b7b7b7b7b7b7b7.jpg', 'https://image.tmdb.org/t/p/w500/5L5z0z9y1b7b7b7b7b7b7b7b7b7.jpg',
        'https://image.tmdb.org/t/p/w500/ycuQaDOcXI6cD0OQxNjcI5b5b5.jpg', 'https://image.tmdb.org/t/p/w500/w2t2z0z9y1b7b7b7b7b7b7b7b7b.jpg',
        'https://image.tmdb.org/t/p/w500/5E5z0z9y1b7b7b7b7b7b7b7b7b7.jpg', 'https://image.tmdb.org/t/p/w500/gKklFOMAqKEZRpzG1iL4A15b5b5.jpg',
        'https://image.tmdb.org/t/p/w500/6FfCGq8i1CcE4nZ1b5b5b5b5b5b.jpg', 'https://image.tmdb.org/t/p/w500/fNOH9f1aA7XRTzl1sAOS9i5b5b5.jpg',
        'https://image.tmdb.org/t/p/w500/78lPtwv72eTNqRQ9nSG5b5b5b5b.jpg', 'https://image.tmdb.org/t/p/w500/r7vmZjiyZw9rpJMQJeq1b5b5b5b.jpg',
        'https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO1b5b5b5b.jpg', 'https://image.tmdb.org/t/p/w500/qvktm0BHcnmDcmpiw5b5b5b5b5b.jpg',
        'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1sX1T5b5b5b5b5.jpg', 'https://image.tmdb.org/t/p/w500/3b3z0z9y1b7b7b7b7b7b7b7b7b7.jpg',
        'https://image.tmdb.org/t/p/w500/4b4z0z9y1b7b7b7b7b7b7b7b7b7.jpg', 'https://image.tmdb.org/t/p/w500/5b5z0z9y1b7b7b7b7b7b7b7b7b7.jpg'
    ],
    'trailer':[
        # Generic Youtube search links for the trailers to ensure they work smoothly
        'https://www.youtube.com/embed/zSWdZVtXT7E', 'https://www.youtube.com/embed/K0eDlFX9GMc', 'https://www.youtube.com/embed/TcMBFSGVi1c', 
        'https://www.youtube.com/embed/x_7YlGv9u1g', 'https://www.youtube.com/embed/EXeTwQWrcwY', 'https://www.youtube.com/embed/fjbZAdGOOAA',
        'https://www.youtube.com/embed/YoHD9XEInc0', 'https://www.youtube.com/embed/vqu4z34wENw', 'https://www.youtube.com/embed/n9xhJrPXop4',
        'https://www.youtube.com/embed/t06RUxPbpMAC', 'https://www.youtube.com/embed/hTjXpQ-tG10', 'https://www.youtube.com/embed/5PSNL1qE6VY',
        'https://www.youtube.com/embed/COv52Qyctws', 'https://www.youtube.com/embed/vKQi3bBA1y8', 'https://www.youtube.com/embed/Qah9sSIXJqk',
        'https://www.youtube.com/embed/G62HrubdD6o', 'https://www.youtube.com/embed/zAGVQLHvwOY', 'https://www.youtube.com/embed/kVrqfYjkTdQ',
        'https://www.youtube.com/embed/Rbp2XUWaqaM', 'https://www.youtube.com/embed/NgBoKJyTgYo', 'https://www.youtube.com/embed/uYPbbksJxIg',
        'https://www.youtube.com/embed/SOXWc32k4zA', 'https://www.youtube.com/embed/QcgJEAo9n-Y', 'https://www.youtube.com/embed/hO2xXh7A2pA',
        'https://www.youtube.com/embed/owK1qxDselE', 'https://www.youtube.com/embed/OiTiKOy59o4',
        # New Additions
        'https://www.youtube.com/embed/C0BMx-qxsP4', 'https://www.youtube.com/embed/DydmpctQ-A0', 'https://www.youtube.com/embed/pKctjlrbEkQ',
        'https://www.youtube.com/embed/11091tQ2Hok', 'https://www.youtube.com/embed/vyX4toD395U', 'https://www.youtube.com/embed/AuuX2j14Jsc',
        'https://www.youtube.com/embed/oSIGQ0YkFcg', 'https://www.youtube.com/embed/NCGAcwNQxng', 'https://www.youtube.com/embed/vKQi3bBA1y8',
        'https://www.youtube.com/embed/2iVYI99VGaw', 'https://www.youtube.com/embed/ONHBaC-pfsk', 'https://www.youtube.com/embed/tcdUhdOlz9M',
        'https://www.youtube.com/embed/ej3ioOneTy8', 'https://www.youtube.com/embed/gCcx85zbxz4', 'https://www.youtube.com/embed/vZ734NWnAHA',
        'https://www.youtube.com/embed/qvsgGtivCgs', 'https://www.youtube.com/embed/8ugaeA-nMBc', 'https://www.youtube.com/embed/d96cjJhvlMA',
        'https://www.youtube.com/embed/hEJnMQG9ev8', 'https://www.youtube.com/embed/k64P4l2Wmeg', 'https://www.youtube.com/embed/JfVOs4VSpmA',
        'https://www.youtube.com/embed/y13dzT7w7zE', 'https://www.youtube.com/embed/bXv41QeS-w0', 'https://www.youtube.com/embed/1J76wN0TPI4'
    ]
}

pd.DataFrame(movies).to_csv('datasets/movies.csv', index=False)
print("Massive 50-Movie Dataset Generated Successfully! Ready to stream.")