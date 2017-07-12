<template>
    <q-layout ref="layout">
        <drawer-head slot="header" title="Scout New Match" @toggleLeft="$refs.layout.toggleLeft()"></drawer-head>
        <drawer-body slot="left"></drawer-body>

        <div class="layout-view">
            <q-pull-to-refresh :handler="refresher" :distance="15" pull-message="Pull to Fetch Another Quote" refresh-message="Quoting.." release-message="Release to Fetch Another Quote">
                <div class="layout-padding">
                    <blockquote>
                        <p class="literal">{{ quoteText }}</p>
                        <small>{{ quoteAttributedTo }}</small>
                    </blockquote>
                    <hr>
                    <q-btn color="primary" class="full-width" @click="createMatch()" no-caps>Begin Scouting!</q-btn>
                </div>
            </q-pull-to-refresh>
        </div>
    </q-layout>
</template>

<script>
    import DrawerHead from '../Drawer/Head.vue'
    import DrawerBody from '../Drawer/Body.vue'
    import store from '../../store.js'
    import * as matchActions from '../../actions/matches.js'
    import * as util from '../../util.js'
    import {
        QPullToRefresh,
        QLayout,
        QBtn
    } from 'quasar'

    const quotes = [
        {text: 'Everything popular is wrong.', attributedTo: 'Oscar Wilde'},
        {text: 'Don\'t cry because it\'s over, smile because it happened.', attributedTo: 'Dr. Seuss'},
        {text: 'Be yourself; everyone else is already taken.', attributedTo: 'Oscar Wilde'},
        {text: 'Two things are infinite: the universe and human stupidity; and I\'m not sure about the universe.', attributedTo: 'Albert Einstein'},
        {text: 'So many books, so little time.', attributedTo: 'Frank Zappa'},
        {text: 'Those who cannot remember the past are condemned to repeat it', attributedTo: 'George Santayana'},
        {text: 'Only the dead have seen the end of war', attributedTo: 'George Santayana'},
        {text: 'If desire is the root of suffering, is the creation of objects designed purely for pleasure ethical?', attributedTo: '@halsted'},
        {text: 'Trouble shared is trouble halved.', attributedTo: 'Lee Iacocca'},
        {text: 'A room without books is like a body without a soul.', attributedTo: 'Marcus Tullius Cicero'},
        {text: 'You only live once, but if you do it right, once is enough.', attributedTo: 'Mae West'},
        {text: 'Be the change that you wish to see in the world.', attributedTo: 'Mahatma Gandhi'},
        {text: 'Don\'t walk in front of me… I may not follow.\nDon\'t walk behind me… I may not lead.\nWalk beside me… just be my friend.', attributedTo: 'Albert Camus'},
        {text: 'No one can make you feel inferior without your consent.', attributedTo: 'Eleanor Roosevelt'},
        {text: 'If you tell the truth, you don\'t have to remember anything.', attributedTo: 'Mark Twain'},
        {text: 'I\'ve learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.', attributedTo: 'Maya Angelou'},
        {text: 'It\'s one of the greatest gifts you can give yourself, to forgive. Forgive Everybody.', attributedTo: 'Maya Angelou'},
        {text: 'Uhhh....Strap???', attributedTo: 'Team 125 - Nutrons'},
        {text: 'Education is what remains after one has forgotten what one has learned in school.', attributedTo: 'Albert Einstein'},
        {text: 'Nothing is more dangerous than an idea, when it\'s the only one we have.', attributedTo: 'Alain'},
        {text: 'Mentor Built, Student Watched.', attributedTo: 'Team 1254 - The Chez Cakes'},
        {text: 'Delicious and nutritious!', attributedTo: 'Team 254 - The Cheesy Poofs'},
        {text: 'Always forgive your enemies; nothing annoys them so much.', attributedTo: 'Oscar Wilde'},
        {text: 'Live as if you were to die tomorrow. Learn as if you were to live forever.', attributedTo: 'Mahatma Gandhi'},
        {text: 'Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that.', attributedTo: 'Martin Luther King Jr.'},
        {text: 'Here\'s to the crazy ones. The misfits. The rebels. The troublemakers. The round pegs in the square holes. The ones who see things differently. They\'re not fond of rules. And they have no respect for the status quo. You can quote them, disagree with them, glorify or vilify them. About the only thing you can\'t do is ignore them. Because they change things. They push the human race forward. And while some may see them as the crazy ones, we see genius. Because the people who are crazy enough to think they can change the world, are the ones who do.', attributedTo: 'Rob Siltanen'},
        {text: 'To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.', attributedTo: 'Ralph Waldo Emerson'},
        {text: 'Insanity is doing the same thing, over and over again, but expecting different results.', attributedTo: 'Narcotics Anonymous'},
        {text: 'It is better to be hated for what you are than to be loved for what you are not.', attributedTo: 'André Gide'},
        {text: 'There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.', attributedTo: 'Albert Einstein'},
        {text: 'It is better to remain silent at the risk of being thought a fool, than to talk and remove all doubt of it.', attributedTo: 'Maurice Switzer'},
        {text: 'Life is what happens to us while we are making other plans.', attributedTo: 'Allen Saunders'},
        {text: 'BERT I\'m your biggest fan', attributedTo: 'Willette'},
        {text: 'The fool doth think he is wise, but the wise man knows himself to be a fool.', attributedTo: 'William Shakespeare'},
        {text: 'You can\'t connect the dots looking forward you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future. You have to trust in something: your gut, destiny, life, karma, whatever. Because believing that the dots will connect down the road will give you the confidence to follow your heart, even when it leads you off the well worn path.', attributedTo: 'Steve Jobs'},
        {text: 'We are all in the gutter, but some of us are looking at the stars.', attributedTo: 'Oscar Wilde'},
        {text: 'I have not failed. I\'ve just found 10,000 ways that won\'t work.', attributedTo: 'Thomas A. Edison'},
        {text: 'If you don\'t stand for something you will fall for anything.', attributedTo: 'Gordon A. Eadie'},
        {text: 'The man who does not read has no advantage over the man who cannot read.', attributedTo: 'Mark Twain'},
        {text: 'I may not have gone where I intended to go, but I think I have ended up where I needed to be.', attributedTo: 'Douglas Adams'},
        {text: 'Sometimes the right path is not the easiest one.', attributedTo: 'Grandmother Willow'},
        {text: 'You know you\'re in love when you can\'t fall asleep because reality is finally better than your dreams.', attributedTo: 'Dr. Seuss'},
        {text: 'Commitment is an act, not a word.', attributedTo: 'Jean-Paul Sartre'},
        {text: 'If you judge people, you have no time to love them.', attributedTo: 'Mother Teresa'},
        {text: 'For every minute you are angry you lose sixty seconds of happiness.', attributedTo: 'Ralph Waldo Emerson'},
        {text: 'A reader lives a thousand lives before he dies, said Jojen. The man who never reads lives only one.', attributedTo: 'George R.R. Martin'},
        {text: 'It is never too late to be what you might have been.', attributedTo: 'George Eliot'},
        {text: 'I love deadlines. I love the whooshing noise they make as they go by.', attributedTo: 'Douglas Adams'},
        {text: 'I\'m not upset that you lied to me, I\'m upset that from now on I can\'t believe you.', attributedTo: 'Friedrich Nietzsche'},
        {text: 'If you only read the books that everyone else is reading, you can only think what everyone else is thinking.', attributedTo: 'Haruki Murakami'},
        {text: 'Folks are usually about as happy as they make their minds up to be.', attributedTo: 'Abraham Lincoln'},
        {text: 'Life isn\'t about finding yourself. Life is about creating yourself.', attributedTo: 'George Bernard Shaw'},
        {text: 'The difference between genius and stupidity is: genius has its limits.', attributedTo: 'Alexandre Dumas fils'},
        {text: 'I find television very educating. Every time somebody turns on the set, I go into the other room and read a book.', attributedTo: 'Groucho Marx'},
        {text: 'When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us.', attributedTo: 'Helen Keller'},
        {text: 'The trouble with having an open mind, of course, is that people will insist on coming along and trying to put things in it.', attributedTo: 'Terry Pratchett'},
        {text: 'Not all those who wander are lost.', attributedTo: 'J.R.R. Tolkien'},
        {text: 'Do. Or do not. There is no try.', attributedTo: 'Grand Master of the Jedi High Council and Jedi Order, Yoda'},
        {text: 'I am free of all prejudice. I hate everyone equally.', attributedTo: 'W.C. Fields'},
        {text: 'I have never let my schooling interfere with my education.', attributedTo: 'Mark Twain'},
        {text: '\'Classic\' - a book which people praise and don\'t read.', attributedTo: 'Mark Twain'},
        {text: 'The question isn\'t who is going to let me; it\'s who is going to stop me.', attributedTo: 'Ayn Rand'},
        {text: 'You were the Chosen One! You were supposed to destroy the Sith, not join them. You were supposed to bring balance to the force, not leave it in darkness.', attributedTo: 'Obi-Wan Kenobi'},
        {text: 'But better to get hurt by the truth than comforted with a lie.', attributedTo: 'Khaled Hosseini'},
        {text: '"I wish it need not have happened in my time," said Frodo. "So do I," said Gandalf, "and so do all who live to see such times. But that is not for them to decide. All we have to decide is what to do with the time that is given us.”', attributedTo: 'J.R.R. Tolkien'},
        {text: 'Some day you will be old enough to start reading fairy tales again.', attributedTo: 'C.S. Lewis'},
        {text: 'Question for you. What\'s better than octopus recipe? Answer for you. Eight recipes for octopus.', attributedTo: 'Jian-Yang'},
        {text: 'Erlich, he started crying in Taco Bell. He tried to blame the taco sauce.', attributedTo: 'Jian-Yang'},
        {text: 'I eat the fish.', attributedTo: 'Jian-Yang'},
        {text: 'Just when you think it can\'t get any worse, it can. And just when you think it can\'t get any better, it can.', attributedTo: 'Nicholas Sparks'},
        {text: 'It\'s so hard to forget pain, but it\'s even harder to remember sweetness. We have no scar to show for happiness. We learn so little from peace.', attributedTo: 'Chuck Palahniuk'},
        {text: 'What you\'re supposed to do when you don\'t like a thing is change it. If you can\'t change it, change the way you think about it. Don\'t complain.', attributedTo: 'Maya Angelou'},
        {text: 'Creativity is knowing how to hide your sources', attributedTo: 'C.E.M. Joad'},
        {text: 'The truth will set you free, but first it will piss you off.', attributedTo: 'Joe Klaas'},
        {text: 'I speak to everyone in the same way, whether he is the garbage man or the president of the university.', attributedTo: 'Albert Einstein'},
        {text: 'Happiness is when what you think, what you say, and what you do are in harmony.', attributedTo: 'Mahatma Gandhi'},
        {text: 'Nothing is impossible, the word itself says \'I\'m possible\'!', attributedTo: 'Audrey Hepburn'},
        {text: 'Be curious. Read widely. Try new things. What people call intelligence just boils down to curiosity.', attributedTo: 'Aaron Swartz'},
        {text: 'Think deeply about things. Don’t just go along because that’s the way things are or that’s what your friends say. Consider the effects, consider the alternatives, but most importantly, just think.', attributedTo: 'Aaron Swartz'},
        {text: 'I think deeply about things and want others to do likewise. I work for ideas and learn from people. I don’t like excluding people. I’m a perfectionist, but I won’t let that get in the way of publication. Except for education and entertainment, I’m not going to waste my time on things that won’t have an impact. I try to be friends with everyone, but I hate it when you don’t take me seriously. I don’t hold grudges, it’s not productive, but I learn from my experience. I want to make the world a better place.', attributedTo: 'Aaron Swartz'},
        {text: 'Growing up, I slowly had this process of realizing that all the things around me that people had told me were just the natural way things were, the way things always would be, they weren’t natural at all. They were things that could be changed, and they were things that, more importantly, were wrong and should change, and once I realized that, there was really no going back.', attributedTo: 'Aaron Swartz'},
        {text: 'You only get to see your own perspective. And even our mistakes make sense from our perspective — we see all of the context, everything that led up to it. It all makes sense because we saw it happen. When we screw up, it’s for a reason. When other people screw up, it’s because they’re screwups.', attributedTo: 'Aaron Swartz'},
        {text: 'In other words, instead of providing a place for a group of like-minded people to come together, magazines provide a sampling of what a group of like-minded people might say in such an instance so that you can pretend you’re part of them.', attributedTo: 'Aaron Swartz'},
        {text: 'A leader can never be happy until his people are happy.', attributedTo: 'Genghis Khan'},
        {text: 'It is not sufficient that I succeed - all others must fail.', attributedTo: 'Genghis Khan'},
        {text: 'One arrow alone can be easily broken but many arrows are indestructible.', attributedTo: 'Genghis Khan'},
        {text: 'Turning off an emotion is always a tough decision. I remember how a couple years ago I decided to say goodbye to anger. Sure, anger has its bright moments — you haven’t really lived until you’ve known that special joy of hurling a chair across the room — but it’s also quite time-consuming. Every time someone comes up and hits you, you have to run around chasing after them. And once you start getting angry it’s hard to stop — an angry person doesn’t really want to calm down, it sort of enjoys being angry. So I finally decided to get rid of the whole thing. And you know what? I haven’t regretted the decision one bit.', attributedTo: 'Aaron Swartz'},
        {text: 'Regret — that’s another interesting emotion. I mean, what purpose does it really serve? “There’s no use crying over spilled milk,” my mom once told me when I started sobbing after I got milk all over the floor while trying to make cereal. “I suppose that’s true,” I replied between sobs. “Although maybe my tears will dilute the milk and make it stick to the floor less.” But I was wrong — the milk stayed just as sticky. So maybe regret should be the next one to go.', attributedTo: 'Aaron Swartz'},
        {text: 'But actually, I think it’s going to be frustration. It’s not discussed much, but frustration is really quite distracting. You’re trying to solve some difficult problem but it’s just not working. Instead of taking a moment to try and think of the solution, you just keep getting more and more frustrated until you start jumping up and down and smashing various things. So not only do you waste time jumping, but you also have to pay to replace the stuff you smashed. It’s really a net loss.', attributedTo: 'Aaron Swartz'},
        {text: 'I want to feel nostalgic, I want to feel like there’s this place, just a couple subway stops away, where everything will be alright. A better place, a place I should be in, a place I can go back to. But even just visiting it, the facts are plain. It doesn’t exist, it never has. I’m nostalgic for a place that never existed.', attributedTo: 'Aaron Swartz'},
        {text: 'do no harm permanently', attributedTo: '2602:306:305c:aec0:d9cf:5016:278b:387e'},
        {text: 'I\'m not a fan of signing yearbooks. Why would you get the signature of someone you(\'ll) see on a regular basis? And if you (d/w)on\'t, then are they really your friend? Therefor only strangers should sign your yearbook, and why would you want a stranger\'s signature‽', attributedTo: 'John'}
    ]

    export default {
        mounted () {
            let self = this
            let quote = quotes[Math.floor(Math.random() * quotes.length)]
            self.quoteText = quote.text
            self.quoteAttributedTo = quote.attributedTo
        },
        methods: {
            refresher (done) {
                let self = this
                let quote = quotes[Math.floor(Math.random() * quotes.length)]
                self.quoteText = quote.text
                self.quoteAttributedTo = quote.attributedTo
                done()
            },
            createMatch () {
                let self = this
                store.dispatch(matchActions.createMatch(self.matchID))
                console.info('%cNewMatch: %cCreated Match %O: %O', 'color: blue', 'color: black', self.matchID, matchActions.fetchMatch(self.$select('matches'), self.matchID))
                console.info('%cNewMatch: %cRedirecting to scout page', 'color: blue', 'color: black')
                self.$router.push(`/scout/edit/${self.matchID}`)
            }
        },
        components: {
            QLayout,
            QPullToRefresh,
            QBtn,
            DrawerHead,
            DrawerBody
        },
        data () {
            return {
                matchID: util.generateUUID4(),
                quoteText: '',
                quoteAttributedTo: ''
            }
        }
    }
</script>

<style>
    .literal {
        white-space: pre-wrap
    }
</style>
