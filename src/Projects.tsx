import React from 'react';

type ProjectSectionProps = {
  id: string,
  title: string,
  children?: React.ReactNode,
}

function ProjectSection({id, title, children}: ProjectSectionProps) {
  return (
    <div className='project-section' id={id}>
      <h2>{title}</h2>

      {children}
    </div>
  );
}

export default function Projects(_props: {}) {
  return (
    <>
      <div className="col-1 col-md-2 col-lg-3"/>
      <div className="col-10 col-md-8 col-lg-6">
        <div className='lander-plate' style={{width: '100%'}}>
          <h1 style={{marginBottom: 0}}>Projects</h1>
        </div>

        <ProjectSection id={'thesis'} title={'Thesis'}>
          <p>
            From Fall 2019 to Spring 2020 I worked on my Haverford senior thesis, which was submitted to both the linguistics
            and computer science departments. It investigated the usage of transfer learning between unrelated languages
            to augment neural morphology models. You can find it, including the full PDF,{' '}
            <a href="https://github.com/cstuartroe/thesis">on GitHub</a>.
          </p>
        </ProjectSection>

        <ProjectSection id={'pl'} title={'Programming Languages'}>
          <p>
            I'm an enthusiast of programming languages and programming language theory. I've written non-trivial code
            in <b>Python</b>, <b>Java</b>, <b>C++</b>, <b>Ruby</b>, <b>JavaScript</b>, <b>TypeScript</b>, <b>Golang</b>
            , <b>Haskell</b>, and <b>Scala</b>. Hopefully <b>Rust</b>, <b>OCaml</b>, and <b>Idris</b> will soon make
            appearances on this list.
          </p>

          <p>
            I also design programming languages and programming language-adjacent things. These include{' '}
            <a href="https://github.com/cstuartroe/teko">Teko</a>, an in-progress statically typed scripting language
            whose selling points include structural typing; <a href="https://github.com/cstuartroe/azor">Azor</a>,
            a toy functional language; and <a href="https://github.com/cstuartroe/tson">TSON</a>, a statically-typed
            data interchange format that's a superset of JSON.
          </p>
        </ProjectSection>

        <ProjectSection id={'music'} title={'Music'}>
          <p>
            I'm a casual musician, playing guitar, keys, and my{' '}
            <a href="https://novationmusic.com/en/launch/launchpad-pro">Launchpad</a>.
            I enjoy theory and composition, and my outlook on music is indebted to online educators including{' '}
            <a href="https://www.youtube.com/channel/UCnkp4xDOwqqJD7sSM3xdUiQ">Adam Neely</a>
            , <a href="https://www.youtube.com/channel/UCTUtqcDkzw7bisadh6AOx5w">12Tone</a>
            , <a href="https://www.youtube.com/channel/UCdcemy56JtVTrsFIOoqvV8g">Andrew Huang</a>
            , <a href="https://www.youtube.com/channel/UCz2iUx-Imr6HgDC3zAFpjOw">David Bennett</a>
            , <a href="https://www.youtube.com/channel/UC_Oa7Ph3v94om5OyxY1nPKg">Paul Davids</a>
            , and <a href="https://www.youtube.com/channel/UCRDDHLvQb8HjE2r7_ZuNtWA">Jake Lizzio</a>.
          </p>

          <p>
            In particular, I'm very interested in the theory of tonality (including microtonality) and musical scales.
            I've done a lot of computational music theory work, all of which can be found{' '}
            <a href="https://github.com/cstuartroe/scale-theory">here</a>, a command-line tool with utilities for searching
            for and analyzing tuning systems, chords, and scales, as well as ear training exercises in standard tuning
            and microtonal tunings.
          </p>

          <p>
            In May 2021, my housemates and I made <a href={"https://dwigt.bandcamp.com/album/p-can-weend"}>an EP</a>{' '}
            in 48 hours. No claims are made regarding its quality.
          </p>
        </ProjectSection>

        <ProjectSection id={'language'} title={'Language Learning'}>
          <p>
            I enjoy learning languages for fun. Besides English, which I speak natively, I am also a proficient reader and
            rusty but competent conversationalist with <b>Dutch</b> as well as moderately comfortable in <b>Mandarin</b>. I
            have the terrible habit of casually learning many languages at once, and I have a working familiarity
            (approximately A1-A2 level, or ability to understand given a dictionary) with <b>Spanish</b>, <b>Russian</b>,
            and <b>Turkish</b>. I'm also a casual <b>Esperantist</b> and have attended social events conducted in Esperanto.
          </p>

          <p>
            I can be found on <a href="https://www.duolingo.com/ConorS2pacRoe">Duolingo</a>
            , <a href="https://www.memrise.com/user/%E5%B0%8F%E5%BE%90-csturoe/">Memrise</a>
            , and HelloTalk.
          </p>
        </ProjectSection>

        <ProjectSection id={'writing'} title={'Creative Writing'}>
          <p>
            I've been trying my hand at fiction writing since the beginning of 2019. Here are two selected short pieces:
          </p>

          <p style={{textAlign: 'center'}}>
            <a href="/static/pdf/Eight Minutes.pdf">Eight Minutes</a>
            {' | '}
            <a href="/static/pdf/The Oukkri Toukkri.pdf">The Oukrri Toukkri</a>
          </p>
        </ProjectSection>
      </div>
    </>
  );
}