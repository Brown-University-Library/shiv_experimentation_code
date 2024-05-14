This experimentation stems from a recent brief conversation with colleagues about how to best incorporate small python-scripts that do one thing well into other scripts/workflows.

Typical packaging, where project-A pip-installs script-code-B, _can_ be useful. But anyone who's had to debug errors that are caused by nested packages knows the downsides to such dependencies.

My work with Rust, which produces compiled binaries with no dependencies, inspired me to peruse the landscape of compiled python binaries. Very arguably, I should have spent more time researching before diving in and trying things.

The "research":
- A [brief survey] of options
- [PyInstaller vs py2exe]
- [Shiv vs PEX]
- Where does [Zipapp] fit in?

I eliminated py2exe because it's Windows-specific, and eliminated Zipapp because it doesn't handle library-version dependencies.

I bumped PyInstaller down a bit because one of its "benefits" is that it installs the whole python interpreter, which we don't need on our servers, and which is said to contribute to slow load-times. (It's very possible that one can configure PyInstaller not to do that.)

And I bumped PEX down a bit because I happened to start reading the [Shiv docs] and saw that it appears that Shiv was created at LinkedIn, which would want a performant tool, to overcome some of the limitations of PEX. I had read that PEX uses caching to minimize subsequent-load-times -- but the Shiv docs made it sound like Shiv is still as fast or faster than PEX.

So, this little demo uses basic python code, with one dependency, `requests`, (and specifically an older version of it, for python3.8x SSL compatibility) installed into a virtual-environment in our typical way. After pip-installing shiv, I was able to cd to the github-directory and run:

```
shiv -c count_orgs -o ../count_hall_hoag_orgs .
```

...to get the stand-alone binary. I've since [included it here] in the repo, since it's not too big. I don't know if github will remove the executable bit on it. If so, re-add it via chmod. And then the usage is just like a unix tool:

```
$ ./count_hall_hoag_orgs
```

I haven't really had much of a chance to evaluate this. I love the wonderful unixy-stand-alone nature of the executable. ~~But I'm used to rust binaries being _blazingly_ fast. Most runs of this executable take almost 3 and a half seconds to do a single API call. Granted, the short testing I've done completely coincided with our repository getting utterly hammered (likely by bots), so badly that it has caused service disruptions. But it makes PEX's caching sound appealing.~~ Initial testing of this binary seemed slow, but that was just because I tested when the repository was being brought down by bot-hammering. With the server-load back to normal, average multiple tests yield a run-time of 0.381 seconds, not bad for a network call.

If we were to pursue this -- and I definitely do think we should explore this more -- I'd _really_ want to incorporate a practice to add a --version flag so that one can easily tell the version of a binary one's using. Why? I've made about three small changes to the python code, but haven't yet updated the binary included in the repo. But there's no way to tell that the binary is out-of-date. In my Rust work, [I figured out] how to incorporate the git-commit right into the binary; a dream-come-true. The skimming I've done indicates that some of these tools allow somewhat similar build-functionality.

Other next steps...

- Due to time, I haven't tested our typical pattern of arg-handling -- but I'm pretty sure it should work as expected.  
- We'd have to figure out dotenv stuff -- but from my skimming, I think that, too, is very do-able.

That's it for now. Exciting stuff!



[brief survey]: <https://chat.openai.com/share/268533cc-3edc-4105-9385-8d4de2483225>
[PyInstaller vs py2exe]: <https://chat.openai.com/share/9217b4a6-0de7-45e0-b9a0-be1fb3472f3a>
[Shiv vs PEX]: <https://chat.openai.com/share/deac4e2a-8965-4f31-ab0c-2157efeca3cf>
[Zipapp]: <https://chat.openai.com/share/919749ba-c4d5-4b56-a9db-28037e89c755>
[Shiv docs]: <https://shiv.readthedocs.io/en/latest/history.html>
[included it here]: <https://github.com/Brown-University-Library/shiv_experimentation_code/tree/main/the_created_binary>
[I figured out]: <https://github.com/birkin/parse_ocr_tracker/blob/05203f1e52502373cd96c8351fb904eb91530985/src/main.rs#L12-L18>
