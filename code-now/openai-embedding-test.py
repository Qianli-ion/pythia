"""
testing script for extrating openai's GPT 3 embedding on title and abstract of a paper
"""
import openai, os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

title_abstract = 'Title: Near Perfect GAN inversion. Abstract: To edit a real photo using Generative Adversarial Networks (GANs), we need a GAN inversion algorithm to identify the latent vector that perfectly reproduces it. Unfortunately, whereas existing inversion algorithms can synthesize images similar to real photos, they cannot generate the identical clones needed in most applications. Here, we derive an algorithm that achieves near perfect reconstructions of photos. Rather than relying on encoder- or optimization-based methods to find an inverse mapping on a fixed generator G(⋅), we derive an approach to locally adjust G(⋅) to more optimally represent the photos we wish to synthesize. This is done by locally tweaking the learned mapping G(⋅) s.t. ∥x−G(z)∥<ϵ, with x the photo we wish to reproduce, z the latent vector, ∥⋅∥ an appropriate metric, and ϵ>0 a small scalar. We show that this approach can not only produce synthetic images that are indistinguishable from the real photos we wish to replicate, but that these images are readily editable. We demonstrate the effectiveness of the derived algorithm on a variety of datasets including human faces, animals, and cars, and discuss its importance for diversity and inclusion.'
out = get_embedding(title_abstract, model='text-embedding-ada-002')
breakpoint()
print(out)