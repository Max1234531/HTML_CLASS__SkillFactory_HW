
#модуль с основным кодом, там реализованы все наши классы
from Tags import HTML, TopLevelTag, Tag
        


#полная копия кода SkillFactory (https://gist.github.com/shrimpsizemoose/ea39766e0e9163674ca662f8557e4930)
if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body

#и таки-да, все полноценно работает


        



